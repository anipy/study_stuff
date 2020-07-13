"""UDP client for metrics monitoring"""

import argparse
import logging
import re
import socket
import threading
import time
from collections import namedtuple
from typing import List

import psutil

from client_helper import MetricCollector
from client_helper import Size

NAME = "udp_client"
VERSION = "0.0.1"
EPILOG = "(c) Andrei Nikonov 2020"
DESCRIPTION = """Script to gather disc usage metric and send it to
                 log server."""

LOG_FORMAT = "%(asctime)s: [%(levelname)s] - %(message)s"
formatter = logging.Formatter(fmt=LOG_FORMAT)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger = logging.getLogger("client")
logger.setLevel(logging.WARNING)
logger.addHandler(console_handler)

DiscUsage = namedtuple("DiscUsage", ["mountpoint", "used", "total", "percentage"])

CLIENT_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


def __validate_args(passed_args: dict):
    """Check if all passed arguments valid

    Args:
      passed_args: a dictionary representing passed args and their values

    Raises:
      Any Exception occurred while validation

    """

    host = passed_args.get("host")
    port = passed_args.get("port")
    delay = passed_args.get("delay")

    if re.fullmatch(r"[\w.-]+", host):
        pass
    else:
        raise ValueError(
            "Invalid host. Please use IP address or domain name (eg. `example.com`, `127.0.0.1`"
        )

    if 1024 <= port <= 65535:
        pass
    else:
        raise ValueError("Invalid port. Please use number 1024..65535")

    if delay > 0:
        pass
    else:
        raise ValueError("Delay should be positive number.")


def get_args():
    """Parse values from arguments"""

    prs = argparse.ArgumentParser(prog=NAME, description=DESCRIPTION, epilog=EPILOG)

    prs.add_argument(
        "--host",
        help="server name or ip address to send collected metrics",
        default="localhost",
        type=str,
    )

    prs.add_argument(
        "--port",
        help="port on server to send collected metrics",
        default=42069,
        type=int,
    )

    prs.add_argument(
        "--delay", help="delay between sending metrics", default=60, type=int
    )

    prs.add_argument(
        "-v",
        "--version",
        action="version",
        help="get version of program",
        version=f"%(prog)s {VERSION}"
    )

    prs.add_argument("--verbose", help="enable verbose mode", action="store_true")

    return prs.parse_args()


def send_stats(stats: str, host: str, port: int):
    """Sending stats to server

    Args:
      stats: string containing metrics value

      host: an url or ip address of server

      port: server port
    """
    CLIENT_SOCKET.sendto(stats.encode("utf-8"), (host, port))
    logger.info("%s", f"Sending stats: {stats}")


def disc_usage() -> List[DiscUsage]:
    """Function to get stats of disc partitions usage"""

    def gen_stat():
        for prt in psutil.disk_partitions():
            du_percent = psutil.disk_usage(prt.mountpoint).percent
            du_total = psutil.disk_usage(prt.mountpoint).total
            du_used = psutil.disk_usage(prt.mountpoint).used

            yield DiscUsage(prt.mountpoint, du_used, du_total, du_percent)

    return list(gen_stat())


def consume_collector(collector: MetricCollector, delay: int, host: str, port: int):
    """Consume collector to monitor metrics

    Args:
      collector: a MetricCollector observing metric

      delay: a delay between sending metrics to server

      host: url or ip of server

      port: serer port

    """
    logger.debug("%s", f"Consume collector: {collector}")

    while True:
        metric_name, metric_value = collector.get_current_state()

        if metric_value:
            for stats in metric_value:
                pretty_stats = f"{stats.mountpoint} " \
                               f":{Size(stats.used, True)}" \
                               f"/{Size(stats.total, True)} ({stats.percentage}%)"
                send_stats(f"{metric_name}, {pretty_stats}", host, port)
        else:
            logger.warning("No metric value yet.")

        time.sleep(delay)


if __name__ == "__main__":
    args = get_args()
    __validate_args(args.__dict__)

    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logger.debug("%s", f"Passed args: {args.__dict__}")

    mc_disc_usage = MetricCollector("disc_usage", disc_usage)
    collect_thread = threading.Thread(target=mc_disc_usage.start_collect)
    collect_thread.daemon = True
    collect_thread.start()

    consume_collector(mc_disc_usage, args.delay, args.host, args.port)
