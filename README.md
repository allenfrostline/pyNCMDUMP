### Update `ncm_converter.py` file (Feb 2025)

Changes:
1. The [PyCrypto](https://www.pycrypto.org) package is no longer activaly maintained. So the latest version change to the [Cryptography](https://pypi.org/project/cryptography/), which can be installed through `pip install cryptography`.
2. Added some additional command line options support. You can now choose the target folder you want to output to, and the timestamps to only process files created after this time.

```
$ python3 ncmdump.py --help


  usage: ncmdump.py [-h] [-w] paths [paths ...]

  pyNCMDUMP command-line interface

  positional arguments:
    paths            one or more paths to source files

  optional arguments:
      -h, --help            show this help message and exit
      -w , --workers        parallel convertion when set to more than 1 workers (default: 1)
      -t , --target-folder
                        optional target folder for converted files (default: same as source file)
      -a , --after          optional timestamp in yymmddhhmm format to only process files created after this time
```

# pyNCMDUMP

This is a simple commandline tool that helps you convert an encrypted `.ncm` file into its original, more commonly seen audio types (e.g. `flac` and `mp3`). 

## Dependencies

- Python3
- [TQDM](https://github.com/tqdm/tqdm) package, which can be installed through `pip3 install tqdm`
- [PyCrypto](https://www.pycrypto.org) package, which can be installed through `pip3 install pycrypto`

## Usage

The usage would require basic knowledge of running Python3 in a terminal (long/short arguments are inter-changable in examples below):

```
$ python3 ncmdump.py --help


  usage: ncmdump.py [-h] [-w] paths [paths ...]

  pyNCMDUMP command-line interface

  positional arguments:
    paths            one or more paths to source files

  optional arguments:
    -h, --help       show this help message and exit
    -w , --workers   parallel convertion when set to more than 1 workers (default: 1)
```

Example of single-worker mode (default):

```
$ python ncmdump.py A b.ncm


  INFO [2022-10-03 21:13:30] 
  INFO [2022-10-03 21:13:30]            _  _  ___ __  __ ___  _   _ __  __ ___
  INFO [2022-10-03 21:13:30]  _ __ _  _| \| |/ __|  \/  |   \| | | |  \/  | _ \
  INFO [2022-10-03 21:13:30] | '_ \ || | .` | (__| |\/| | |) | |_| | |\/| |  _/
  INFO [2022-10-03 21:13:30] | .__/\_, |_|\_|\___|_|  |_|___/ \___/|_|  |_|_|  
  INFO [2022-10-03 21:13:30] |_|   |__/                                        
  INFO [2022-10-03 21:13:30]                     pyNCMDUMP                     
  INFO [2022-10-03 21:13:30]     https://github.com/allenfrostline/pyNCMDUMP  
  INFO [2022-10-03 21:13:30] 
  INFO [2022-10-03 21:13:30] Running pyNCMDUMP on single-worker mode
  INFO [2022-10-03 21:13:30] Converting "A/a1.ncm"                                                                                                  
  INFO [2022-10-03 21:13:32] Converted file saved at "a1.mp3"                                                                                                   
  INFO [2022-10-03 21:13:32] Converting "A/a2.ncm"                                                                                                      
  INFO [2022-10-03 21:13:35] Converted file saved at "a2.mp3"                                                                                                       
  INFO [2022-10-03 21:13:35] Converting "A/a3.ncm"                                                                                                         
  INFO [2022-10-03 21:13:38] Converted file saved at "a3.mp3"                                                                                                          
  INFO [2022-10-03 21:13:38] Converting "A/a4.ncm"                                                                                               
  INFO [2022-10-03 21:13:45] Converted file saved at "a4.flac"                                                                                               
  INFO [2022-10-03 21:13:45] Converting "b.ncm"                                                                                                                            
  INFO [2022-10-03 21:13:56] Converted file saved at "b.flac"                                                                                                              
  INFO [2022-10-03 21:13:56] All finished 
```

Example of parallel mode using 4 workers:

```
$ python ncmdump.py A b.ncm --workers 4


  INFO [2022-10-03 21:14:04] 
  INFO [2022-10-03 21:14:04]            _  _  ___ __  __ ___  _   _ __  __ ___
  INFO [2022-10-03 21:14:04]  _ __ _  _| \| |/ __|  \/  |   \| | | |  \/  | _ \
  INFO [2022-10-03 21:14:04] | '_ \ || | .` | (__| |\/| | |) | |_| | |\/| |  _/
  INFO [2022-10-03 21:14:04] | .__/\_, |_|\_|\___|_|  |_|___/ \___/|_|  |_|_|  
  INFO [2022-10-03 21:14:04] |_|   |__/                                        
  INFO [2022-10-03 21:14:04]                     pyNCMDUMP                     
  INFO [2022-10-03 21:14:04]     https://github.com/allenfrostline/pyNCMDUMP  
  INFO [2022-10-03 21:14:04] 
  INFO [2022-10-03 21:14:04] Running pyNCMDUMP with up to 4 parallel workers
  INFO [2022-10-03 21:14:04] Converting "A/a1.ncm"
  INFO [2022-10-03 21:14:04] Converting "A/a2.ncm"
  INFO [2022-10-03 21:14:04] Converting "A/a4.ncm"
  INFO [2022-10-03 21:14:04] Converting "A/a3.ncm"
  INFO [2022-10-03 21:14:07] Converted file saved at "a1.mp3"
  INFO [2022-10-03 21:14:07] Converting "b.ncm"
  INFO [2022-10-03 21:14:07] Converted file saved at "a3.mp3"
  INFO [2022-10-03 21:14:07] Converted file saved at "a2.mp3"
  INFO [2022-10-03 21:14:11] Converted file saved at "a4.flac"
  INFO [2022-10-03 21:14:17] Converted file saved at "b.flac"
  INFO [2022-10-03 21:14:17] All finished
```

Credit to [anonymous5l](https://github.com/anonymous5l), who wrote the original version of [ncmdump](https://github.com/anonymous5l/ncmdump) in C++.
