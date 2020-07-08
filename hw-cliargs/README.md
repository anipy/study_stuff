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
 