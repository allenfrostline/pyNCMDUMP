import base64
import binascii
import glob
import json
import os
import struct
import sys

from time import sleep
from multiprocessing import Pool, cpu_count
from random import uniform
from Crypto.Cipher import AES


def existing_mp3(file_path):
    file_name = os.path.splitext(file_path)[0]
    return os.path.exists(file_name + ".mp3") or os.path.exists(file_name + ".flac")


def dump(file_path):
    if existing_mp3(file_path):
        print('[Error]转换文件已存在，跳过\n')
        return
    print(f"[Dump]正在处理文件 {file_path}")
    # hex to str
    core_key = binascii.a2b_hex("687A4852416D736F356B496E62617857")
    meta_key = binascii.a2b_hex("2331346C6A6B5F215C5D2630553C2728")
    unpad = lambda s: s[0:-(s[-1] if type(s[-1]) is int else ord(s[-1]))]
    f = open(file_path, 'rb')
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
    file_name = f.name.split("/")[-1].split(".ncm")[0] + '.' + meta_data['format']
    m = open(os.path.join(os.path.split(file_path)[0], file_name), 'wb')
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
    m.close()
    f.close()
    print(f"[Dump] {file_path} 已完成")
    return file_name


def go_dump(f_list):
    for f in f_list:
        print(f'[Main] 正在处理文件：{f}')
        dump(f)


def main(t1):
    try:
        for file in t1:
            if os.path.isfile(file):
                print(f'[Main] 正在处理文件：{file}')
                dump(file)
            elif os.path.isdir(file):
                files = glob.glob(os.path.join(os.path.join(file, '**'), '*.ncm'), recursive=True)
                go_dump(files)
    except KeyboardInterrupt:
        return None


if __name__ == '__main__':
    print(
        "            _  _  ___ __  __ ___  _   _ __  __ ___ \n",
        "  _ __ _  _| \| |/ __|  \/  |   \| | | |  \/  | _ \ \n",
        " | '_ \ || | .` | (__| |\/| | |) | |_| | |\/| |  _/ \n",
        " | .__/\_, |_|\_|\___|_|  |_|___/ \___/|_|  |_|_|   \n",
        " |_|   |__/                                         \n",
        "                     pyNCMDUMP                      \n",
        "     https://github.com/allenfrostline/pyNCMDUMP    \n"
    )
    file_list = sys.argv[1:]
    sleep(uniform(1, 3))
    print("[Init]检测核心数量......")
    cpus = cpu_count()
    sleep(uniform(0, 1))
    print(f"[Init]检测到 {cpus} 个核心。")
    processes = cpus - 1
    sleep(uniform(0, 2))
    print(f"[MXP] 使用 {processes} 个进程。")
    sleep(uniform(0, 1))
    print("[MXP]您可以通过修改源码第 128 行来修改使用的进程数量，但我们不推荐您这样做。")
    sleep(uniform(0, 1))
    print("[MXP]初始化进程池......")
    pool = Pool(processes=processes)
    sleep(uniform(0, 1))
    print("[MXP]初始化线程池完成。")
    sleep(uniform(0, 1))
    print("[Main]开始处理文件......\n")
    if len(file_list) == 1:
        for f in file_list:
            print("[Main]待处理文件 1 个。")
            if os.path.isfile(f):
                main(file_list)
            elif os.path.isdir(f):
                files = glob.glob(os.path.join(os.path.join(f, '**'), '*.ncm'), recursive=True)
                number = len(files)
                print(f"[Main]待处理文件 {number} 个。")
                single = number // processes + 1
                try:
                    for fil in range(0, number, single):
                        single_files = files[fil:fil + number]
                        pool.apply_async(main, (single_files,))
                    pool.close()
                    pool.join()
                except KeyboardInterrupt:
                    pid = os.getpid()
                    os.popen('taskkill.exe /f /pid:%d' % pid)
                except Exception as e:
                    print(e)
    elif len(file_list) > 1:
        number = len(file_list)
        try:
            for f in file_list:
                if os.path.isfile(f):
                    print(f"[Main]待处理文件 {number} 个。")
                    pool.apply_async(main, f)
                elif os.path.isdir(f):
                    # 这会平添很多麻烦。何不直接传入一整个文件夹呢？
                    raise ImportError("不允许在有多个输入时混杂文件夹")
            pool.close()
            pool.join()
        except KeyboardInterrupt:
            pid = os.getpid()
            os.popen('taskkill.exe /f /pid:%d' % pid)
        except Exception as e:
            print(e)
