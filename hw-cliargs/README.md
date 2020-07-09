## README ##

This homework is an exercise to train basic skills with CLI arguments using argparse library.

### How to run ###

* Clone current branch

`$ git clone https://github.com/anipy/study_stuff.git --branch hw-cliargs`

`$ cd study_stuff/hw-cliargs`

`$ python ls.py --help`

### Available arguments ###

```
$ ls --help

usage: ls [-a] [-h] [-l] [-r] [-S] [-t] [-u] [--version] [--debug] [--help] [FILE]

Custom realization for ls utility. But it has a bit of functionality from original one.

positional arguments:
  FILE

optional arguments:
  -a, --all             do not ignore entries starting with .
  -h, --human-readable  with -l print human readable sizes
  -l                    use a long listing format
  -r, --reverse         reverse order while sorting
  -S                    sort by file size, largest first
  -t                    sort by modification time, newest first
  -u                    sort by access time, newest first
  --version             output version information and exit
  --debug               enable debug mode
  --help                show this help message and exit

(c) Andrei Nikonov 2020

 ```
 
 ### Demo ###
 ```
 h:\projects\epam\study_stuff\hw-cliargs>ls
ls.py  ls_helper.py  README.md  __pycache__

h:\projects\epam\study_stuff\hw-cliargs>ls -l
2020-07-09 07:03  drwxrwxrwx  0  __pycache__
2020-07-08 22:29  -rw-rw-rw-  1187  README.md
2020-07-08 22:27  -rw-rw-rw-  2755  ls_helper.py
2020-07-08 22:27  -rw-rw-rw-  7414  ls.py

h:\projects\epam\study_stuff\hw-cliargs>ls ls.py
ls.py

h:\projects\epam\study_stuff\hw-cliargs>ls ls.py -l
2020-07-08 22:27  -rw-rw-rw-  7414  ls.py

h:\projects\epam\study_stuff\hw-cliargs>ls ls.py -lu
2020-07-09 07:17  -rw-rw-rw-  7414  ls.py

h:\projects\epam\study_stuff\hw-cliargs>ls ls.py -lah
2020-07-08 22:27  -rw-rw-rw-  7.24K  ls.py

h:\projects\epam\study_stuff\hw-cliargs>ls ../ -lahSu --debug
Got arguments: {'all': False, 'human_readable': True, 'independent': ['long'], 'sorting': ['size', 'atime'], 'debug': True, 'inspect_catalog': '../'}
Independent options provided: ['long']
Sorting options provided: ['size', 'atime']
Considering which time to show from: ['size', 'atime']
sorting: ['size', 'atime']
Scanning directory: ../
2020-07-08 22:38  drwxrwxrwx  8.00K  hw-multithreading
2020-07-08 22:39  drwxrwxrwx  4.00K  .git
2020-07-08 22:38  drwxrwxrwx  4.00K  hw-pandas
2020-07-08 22:38  -rw-rw-rw-  1.88K  .gitignore
2020-07-08 22:38  -rw-rw-rw-  650.00B  README.md
2020-07-09 07:17  drwxrwxrwx  0B  hw-cliargs
2020-07-08 22:38  drwxrwxrwx  0B  hw-testing
```
