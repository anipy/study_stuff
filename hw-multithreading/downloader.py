"""Script to download images from a file by url, than thumbnail them and save to given directory"""

import argparse
import io
import logging
import os
import sys
from multiprocessing.pool import ThreadPool
from os.path import join
from typing import Tuple

import requests
from PIL import Image

from timer import Timer


NAME = "downloader"
VERSION = "0.0.1"
EPILOG = "(c) Andrei Nikonov 2020"
DESCRIPTION = """Script to download images from a file by url,
                 than thumbnail them and save to given directory"""
LOG_FORMAT = "%(asctime)s: %(thread)d\t[%(levelname)s] - %(message)s"

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)


def __parse_size(size: str) -> Tuple[int, int]:
    """Parse a tuple of height and width from string

    Args:
      size: a string in format 'INTxINT'

    Returns:
      Tuple[int, int]
    """
    return tuple(map(int, size.lower().split("x")))


def __validate_args(passed_args: dict) -> bool:
    """Check if all passed arguments valid

    Args:
      passed_args: a dictionary representing passed args and their values

    Returns:
      True if all validations passed

    Raises:
      Any Exception occurred while validation
    """

    urllist_file = passed_args.get("urllist_filename")
    n_thr = passed_args.get("threads")
    pic_size = passed_args.get("size")
    export_dir = passed_args.get("dir")

    assert (
        1 <= n_thr <= 100
    ), f"Can't create {n_thr} threads. It have to be in range(1, 100)"

    if pic_size:
        try:
            height, width = __parse_size(pic_size)
        except Exception:
            raise

        assert all(
            [side > 0 for side in (height, width)]
        ), "Both height and width have to be positive"

    if export_dir:
        if os.path.exists(export_dir):
            pass
        else:
            try:
                os.mkdir(export_dir)
            except Exception:
                raise

    if urllist_file:
        if os.path.exists(urllist_file[0]):
            pass
        else:
            raise FileNotFoundError(f"Can't find file {urllist_file}")

    return True


def get_args():
    """Parse values from arguments"""

    prs = argparse.ArgumentParser(description=DESCRIPTION,
                                  prog=NAME,
                                  epilog=EPILOG)

    prs.add_argument(
        "urllist_filename",
        metavar="FILE",
        type=str,
        nargs=1,
        help="file containing urls to download",
    )

    prs.add_argument(
        "-t", "--threads", type=int, default=1, help="number of threads to use"
    )

    prs.add_argument(
        "-d",
        "--dir",
        type=str,
        default=os.getcwd(),
        help="path to directory to save downloaded files",
    )

    prs.add_argument(
        "-s",
        "--size",
        type=str,
        default="100x100",
        help="size to scale image in format INTxINT",
    )

    prs.add_argument(
        "-v",
        "--version",
        action="version",
        help="get version of program",
        version=f"%(prog)s {VERSION}"
    )

    return prs.parse_args()


def read_file(path: str):
    """Read file from start to end and yield every new line

    Args:
      path: a path to a file with list of urls
    """
    with open(path) as file:
        for line in file.readlines():
            yield line.strip()


def write_file(path: str, img: bytes, size: Tuple[int, int]) -> bool:
    """Save scaled image to file

    Args:
      path: path where to save file

      img: raw bytes supposed to be an image

      size: height and width to rescale image

    Returns:
      True if operation was successful, False otherwise
    """

    try:
        img_object = Image.open(io.BytesIO(img))
        img_object.thumbnail(size)
        img_object = img_object.convert("RGB")
        img_object.save(path, format="jpeg")
        logger.info("Successfully saved %s", path)
        return True

    except Exception:
        logger.exception('Can\'t save file "%s"', path)
        return False


def download_pic(url: str) -> bytes:
    """Download a picture from url

    Args:
      url: an URL to download

    Returns:
      A raw content if operation was successful else empty bytes object
    """
    try:
        response = requests.get(url)

        if response.status_code == 200:
            logger.info('Success to open url "%s...%s"', url[:20], url[-10:])
            return response.content

        logger.warning('Failed to GET url "%s"', url)
        return bytes()

    except requests.exceptions.ConnectionError:
        logger.exception('Failed to GET url "%s"', url)
        return bytes()


if __name__ == "__main__":
    args = get_args()

    if __validate_args(args.__dict__):
        logger.debug("Passed parameters: %s", args.__dict__)

        with Timer(True):
            with ThreadPool(args.threads) as pool_download:
                download_result = pool_download.map(
                    download_pic, read_file(args.urllist_filename[0])
                )

            save_img_params = [
                (join(args.dir, f"{e+1:0>5}.jpg"), res, __parse_size(args.size))
                for e, res in enumerate(download_result)
            ]

            with ThreadPool(args.threads) as pool_process:
                save_result = pool_process.starmap(write_file, save_img_params)

            pool_download.join()
            pool_process.join()

            download_bytes = sum(map(len, download_result))
            successful = save_result.count(True)
            failed = save_result.count(False)

            print(
                f"Statistics:\n\tDownloaded: {download_bytes/1024/1024:.2f} Mb"
                f"\n\tSuccessful: {successful}"
                f"\n\tFailed    : {failed}"
            )
    sys.exit(0)
