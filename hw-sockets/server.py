"""UDP server to log some metrics"""

import argparse
import socket
import logging


NAME = "udp_server"
VERSION = "0.0.1"
EPILOG = "(c) Andrei Nikonov 2020"
DESCRIPTION = """Script to aggregate metrics and log them to file."""

LOG_FORMAT = '%(asctime)s: [%(levelname)s] - %(message)s'
formatter = logging.Formatter(fmt=LOG_FORMAT)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger = logging.getLogger('server')
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)


def get_args():
    """Parse values from arguments"""

    prs = argparse.ArgumentParser(prog=NAME, description=DESCRIPTION, epilog=EPILOG)

    prs.add_argument(
        "--file",
        help="file to write logs",
        default='server.log',
        type=str
    )

    prs.add_argument(
        "--port",
        help="port to listen",
        default=42069,
        type=int
    )

    prs.add_argument(
        "-v",
        "--version",
        action="version",
        help="get version of program",
        version=f"%(prog)s {VERSION}"
    )

    return prs.parse_args()


def serve(sock: socket.socket):
    """Start listen to socket"""
    logger.info('Starting server')

    while True:
        data, _ = sock.recvfrom(4096)
        logger.info('%s', data.decode('utf-8'))


if __name__ == '__main__':
    args = get_args()

    file_handler = logging.FileHandler(args.file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    SERVER_SOCKET.bind(('0.0.0.0', args.port))

    serve(SERVER_SOCKET)
