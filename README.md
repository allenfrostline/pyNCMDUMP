# pyNCMDUMP

This is a simple commandline tool that helps you convert an encrypted `.ncm` file into its original, more commonly seen audio types (e.g. `flac` and `mp3`). 

## Dependencies

- Python3
- Crypto.Cipher package, which can be installed by `pip3 install pycrypto`

## Usage

The usage would require basic knowledge of running Python3 in a terminal:

```bash
python3 ncmdump.py [files] ...
```

Credit to [anonymous5l](https://github.com/anonymous5l), who wrote the original version of [ncmdump](https://github.com/anonymous5l/ncmdump) in C++.