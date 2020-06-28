import os
import shutil
import uuid
from contextlib import ContextDecorator
from datetime import datetime


class LogFile(ContextDecorator):
    """Class to log runtime information of wrapped function to file.

    Args:
      path: A path-like object to store logs

    """
    __slots__ = ("path", "log_file", "start_time", "running_time")

    def __init__(self, path):
        self.path = path
        self.start_time = None
        self.running_time = None

    def __enter__(self):
        self.start_time = datetime.now()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.running_time = datetime.now() - self.start_time
            with open(self.path, 'a+') as log:
                log.write(
                    f"Start: {self.start_time} | Run: {self.running_time} | An error occured: {exc_value}\n"
                )
        except Exception:
            raise exc_type


class TempDir:
    """Custom implementation for tempdir.

    A context manager to create a temporary directory in the current one and remove it afterwards"""

    def __init__(self):
        self.pwd = os.getcwd()
        self.name = os.path.join(self.pwd, self.__gen_name(TempDir.gen_name()))

    def __gen_name(self, name) -> str:
        """Generate name for a temporary directory.
        If name already exists, generate a new one"""
        dir_name = name

        if os.path.exists(dir_name):
            return self.__gen_name(TempDir.gen_name())
        else:
            return dir_name

    @staticmethod
    def gen_name() -> str:
        """Generate random string"""
        return str(uuid.uuid1())

    def __enter__(self):
        os.mkdir(self.name)
        os.chdir(self.name)
        return self

    def __exit__(self, *exc):
        os.chdir(self.pwd)
        shutil.rmtree(self.name)

    def __repr__(self):
        return f'TempDir(path="{self.name}")'
