"""Custom realization for ls utility. But it has a bit of functionality from original one."""

import argparse
import logging
import os
import stat
from datetime import datetime as dt
from operator import attrgetter
from typing import List, Tuple

from ls_helper import EntryInfo, Size

df = dt.fromtimestamp
dp = dt.strftime
fm = stat.filemode

NAME = "ls"
VERSION = "0.0.1"
EPILOG = "(c) Andrei Nikonov 2020"
DESCRIPTION = """Custom realization for ls utility. \
                 But it has a bit of functionality from original one."""
LOG_FORMAT = "%(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger("%(prog)s")


def get_stat(path: str):
    """Iterate by entries in directory and yield EntryInfo for each one

    Args:
      path: a path to directory to scan
    """

    logger.debug("Scanning directory: %s", path)

    with os.scandir(path) as dir_content:
        for entry in dir_content:
            yield EntryInfo(
                mtime=dp(df(os.stat(entry).st_mtime), "%Y-%m-%d %H:%M"),
                ctime=dp(df(os.stat(entry).st_ctime), "%Y-%m-%d %H:%M"),
                atime=dp(df(os.stat(entry).st_atime), "%Y-%m-%d %H:%M"),
                mode=fm(os.stat(entry).st_mode),
                size_pretty=Size(os.stat(entry).st_size, True),
                size=Size(os.stat(entry).st_size),
                hidden=entry.name.startswith("."),
                name=entry.name,
            )


def solve_sort(arg_seq: List[str]) -> List[str]:
    """Function to set up sorting order.
    It returns argument names allowed to be sorted in order of appearance

    Args:
      arg_seq: passed list of argument names

    Returns:
      A list of unique arguments for sorting
    """
    logger.debug("Sorting options provided: %s", arg_seq)

    if arg_seq:
        return list(dict.fromkeys(arg_seq))
    else:
        return []


def solve_independent(args_seq: List[str]) -> Tuple[bool, bool]:
    """Function to define printable options which are independent.

    Args:
      args_seq: a list of passed argument names

    Returns:
      Booleans representing if 'long format' and 'reverse sorting' were passed
    """
    logger.debug("Independent options provided: %s", args_seq)

    return "long" in args_seq, "reverse" in args_seq


def solve_showtime(args_seq: List[str]) -> str:
    """Function to setup what time to show

    Since there are three different time metrics for entry:
    `atime` - access time, `mtime` - modification time and
    `ctime` - create time, we want to show the one which appears
    in arguments first. This function exists for that

    Args:
      args_seq: a list of argument names

    Returns:
      First appeared 'time sorting' argument.
    """
    logger.debug("Considering which time to show from: %s", args_seq)

    if any(["time" in option for option in args_seq]):
        return list(filter(lambda x: "time" in x, args_seq))[0]

    return str()


def ls(passed: dict):
    """Function to list entries in provided directory (`current dir` by default)

    Args:
      passed: dictionary of passed arguments
    """

    path = passed.get("inspect_catalog") or "."
    long, reverse = solve_independent(passed.get("independent") or [])
    sorting = list(filter(lambda x: x, solve_sort(passed.get("sorting")))) or [
        "ctime",
        "name",
    ]
    s_time = solve_showtime(sorting) or "ctime"

    if path and os.path.exists(path):
        if not os.path.isdir(path):
            logger.debug("Got file as argument: %s", path)

            entry_info = EntryInfo(
                mtime=dp(df(os.stat(path).st_mtime), "%Y-%m-%d %H:%M"),
                ctime=dp(df(os.stat(path).st_ctime), "%Y-%m-%d %H:%M"),
                atime=dp(df(os.stat(path).st_atime), "%Y-%m-%d %H:%M"),
                mode=fm(os.stat(path).st_mode),
                size_pretty=Size(os.stat(path).st_size, True),
                size=Size(os.stat(path).st_size),
                hidden=os.path.basename(path).startswith("."),
                name=os.path.basename(path),
            )
            if long:
                logger.info(
                    "%s", entry_info.build_printable(args.human_readable, s_time, long)
                )
            else:
                logger.info("%s", entry_info.__dict__.get('name'))

            return

    else:
        logger.warning("cannot access '%s': No such file or directory", path)
        return

    if long:
        logger.debug("sorting: %s", sorting)
        for dir_entry in filter(
                lambda x: not x.hidden if args.all else x,
                sorted(get_stat(path), key=attrgetter(*sorting), reverse=not reverse),
        ):
            logger.info(
                "%s", dir_entry.build_printable(args.human_readable, s_time, long)
            )

    else:
        if args.all:
            logger.info(
                "%s", "  ".join(filter(lambda x: not x.startswith("."), os.listdir(path)))
            )
        else:
            logger.info("%s", "  ".join(os.listdir(path)))


def get_args():
    """Parse argument values"""
    prs = argparse.ArgumentParser(add_help=False,
                                  description=DESCRIPTION,
                                  prog=NAME,
                                  epilog=EPILOG)

    prs.add_argument(
        "-a",
        "--all",
        help="do not ignore entries starting with .",
        action="store_false",
    )

    prs.add_argument(
        "-h",
        "--human-readable",
        help="with -l print human readable sizes",
        action="store_true",
    )

    prs.add_argument(
        "-l",
        help="use a long listing format",
        action="append_const",
        dest="independent",
        const="long",
    )

    prs.add_argument(
        "-r",
        "--reverse",
        help="reverse order while sorting",
        action="append_const",
        dest="independent",
        const="reverse",
    )

    prs.add_argument(
        "-S",
        help="sort by file size, largest first",
        action="append_const",
        dest="sorting",
        const="size",
    )

    prs.add_argument(
        "-t",
        help="sort by modification time, newest first",
        action="append_const",
        dest="sorting",
        const="mtime",
    )

    prs.add_argument(
        "-u",
        help="sort by access time, newest first",
        action="append_const",
        dest="sorting",
        const="atime",
    )

    prs.add_argument("--version", help="output version information and exit",
                     action="version", version=f"%(prog)s {VERSION}")

    prs.add_argument("--debug", help="enable debug mode", action="store_true")

    prs.add_argument("--help", help="show this help message and exit", action="help")

    prs.add_argument("inspect_catalog", action="store", metavar="FILE", nargs="?")

    return prs.parse_args()


if __name__ == "__main__":
    args = get_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)

    logger.debug("Got arguments: %s", args.__dict__)
    ls(args.__dict__)
