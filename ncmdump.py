import os
import json
import base64
import struct
import logging
import binascii
from glob import glob
from tqdm.auto import tqdm
from textwrap import dedent
from Crypto.Cipher import AES
from multiprocessing import Pool


class TqdmLoggingHandler(logging.StreamHandler):
    """Avoid tqdm progress bar interruption by logger's output to console"""
    # see logging.StreamHandler.eval method:
    # https://github.com/python/cpython/blob/d2e2534751fd675c4d5d3adc208bf4fc984da7bf/Lib/logging/__init__.py#L1082-L1091
    # and tqdm.write method:
    # https://github.com/tqdm/tqdm/blob/f86104a1f30c38e6f80bfd8fb16d5fcde1e7749f/tqdm/std.py#L614-L620

    def emit(self, record):
        try:
            msg = self.format(record)
            tqdm.write(msg, end=self.terminator)
        except RecursionError:
            raise
        except Exception:
            self.handleError(record)


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
handler = TqdmLoggingHandler()
fmt = '%(levelname)7s [%(asctime)s] %(message)s'
datefmt = '%Y-%m-%d %H:%M:%S'
handler.setFormatter(logging.Formatter(fmt, datefmt))
log.addHandler(handler)


def dump_single_file(filepath):
    try:

        filename = filepath.split('/')[-1]
        if not filename.endswith('.ncm'): return
        filename = filename[:-4]
        for ftype in ['mp3', 'flac']:
            fname = f'{filename}.{ftype}'
            if os.path.isfile(fname):
                log.warning(f'Skipping "{filepath}" due to existing file "{fname}"')
                return

        log.info(f'Converting "{filepath}"')

        # hex to str
        core_key = binascii.a2b_hex('687A4852416D736F356B496E62617857')
        meta_key = binascii.a2b_hex('2331346C6A6B5F215C5D2630553C2728')
        unpad = lambda s: s[0:-(s[-1] if isinstance(s[-1], int) else ord(s[-1]))]
        with open(filepath, 'rb') as f:
            header = f.read(8)
            
            # str to hex
            assert binascii.b2a_hex(header) == b'4354454e4644414d'
            f.seek(2, 1)
            key_length = f.read(4)
            key_length = struct.unpack('<I', bytes(key_length))[0]
            key_data = f.read(key_length)
            key_data_array = bytearray(key_data)
            for i in range(0, len(key_data_array)):
                key_data_array[i] ^= 0x64
            key_data = bytes(key_data_array)
            cryptor = AES.new(core_key, AES.MODE_ECB)
            key_data = unpad(cryptor.decrypt(key_data))[17:]
            key_length = len(key_data)
            key_data = bytearray(key_data)
            key_box = bytearray(range(256))

            c = 0
            last_byte = 0
            key_offset = 0
            for i in range(256):
                swap = key_box[i]
                c = (swap + last_byte + key_data[key_offset]) & 0xff
                key_offset += 1
                if key_offset >= key_length:
                    key_offset = 0
                key_box[i] = key_box[c]
                key_box[c] = swap
                last_byte = c

            meta_length = f.read(4)
            meta_length = struct.unpack('<I', bytes(meta_length))[0]
            meta_data = f.read(meta_length)
            meta_data_array = bytearray(meta_data)
            for i in range(0, len(meta_data_array)):
                meta_data_array[i] ^= 0x63
            meta_data = bytes(meta_data_array)
            meta_data = base64.b64decode(meta_data[22:])
            cryptor = AES.new(meta_key, AES.MODE_ECB)
            meta_data = unpad(cryptor.decrypt(meta_data)).decode('utf-8')[6:]
            meta_data = json.loads(meta_data)

            crc32 = f.read(4)
            crc32 = struct.unpack('<I', bytes(crc32))[0]
            f.seek(5, 1)
            image_size = f.read(4)
            image_size = struct.unpack('<I', bytes(image_size))[0]
            image_data = f.read(image_size)
            target_filename = filename + '.' + meta_data['format']

            with open(target_filename, 'wb') as m:
                chunk = bytearray()
                while True:
                    chunk = bytearray(f.read(0x8000))
                    chunk_length = len(chunk)
                    if not chunk:
                        break
                    for i in range(1, chunk_length + 1):
                        j = i & 0xff
                        chunk[i - 1] ^= key_box[(key_box[j] + key_box[(key_box[j] + j) & 0xff]) & 0xff]
                    m.write(chunk)
        log.info(f'Converted file saved at "{target_filename}"')
        return target_filename

    except KeyboardInterrupt:
        log.warning('Aborted')
        quit()


def list_filepaths(path):
    if os.path.isfile(path):
        return [path]
    elif os.path.isdir(path):
        return [fp for p in glob(f'{path}/*') for fp in list_filepaths(p)]
    else:
        raise ValueError(f'path not recognized: {path}')


def dump(*paths, n_workers=None):
    header = dedent(r'''
                   _  _  ___ __  __ ___  _   _ __  __ ___
         _ __ _  _| \| |/ __|  \/  |   \| | | |  \/  | _ \
        | '_ \ || | .` | (__| |\/| | |) | |_| | |\/| |  _/
        | .__/\_, |_|\_|\___|_|  |_|___/ \___/|_|  |_|_|  
        |_|   |__/                                        
                            pyNCMDUMP                     
            https://github.com/allenfrostline/pyNCMDUMP  
    ''')
    for line in header.split('\n'):
        log.info(line)

    all_filepaths = [fp for p in paths for fp in list_filepaths(p)]
    if n_workers > 1:
        log.info(f'Running pyNCMDUMP with up to {n_workers} parallel workers')
        with Pool(processes=n_workers) as p:
            list(p.map(dump_single_file, all_filepaths))
    else:
        log.info('Running pyNCMDUMP on single-worker mode')
        for fp in tqdm(all_filepaths, leave=False): dump_single_file(fp)
    log.info('All finished')


if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser(description='pyNCMDUMP command-line interface')
    parser.add_argument(
        'paths',
        metavar='paths',
        type=str,
        nargs='+',
        help='one or more paths to source files'
    )
    parser.add_argument(
        '-w', '--workers',
        metavar='',
        type=int,
        help=f'parallel convertion when set to more than 1 workers (default: 1)',
        default=1
    )
    args = parser.parse_args()
    dump(*args.paths, n_workers=args.workers)
