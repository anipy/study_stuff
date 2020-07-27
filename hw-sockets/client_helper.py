"""Helper classes for client part.

MetricCollector: Class to collect metrics. You have to define a
  function able to return value to use this class.

Size: Class to handle file size and pretty print it.

"""

import functools
from collections import OrderedDict
from time import sleep
from typing import Callable


class MetricCollectorIsRunningError(Exception):
    def __str__(self):
        return "MetricCollector is already running"


class MetricCollectorIsStoppedError(Exception):
    def __str__(self):
        return "MetricCollector is already stopped"


class MetricCollector:
    """Class to collect metrics

    Args:
      name: name of metric

      target_function: function to call to get metric

    """

    def __init__(self, name: str, target_function: Callable):
        self.name = name
        self.target_function = target_function
        self.value = None
        self._active = False

    def start_collect(self):
        """Begin observe metric"""
        if self._active:
            raise MetricCollectorIsRunningError
        else:
            self._active = True

        while self._active:
            self.value = self.target_function()
            sleep(1)  # for saving CPU usage

    def get_current_state(self):
        """Get current state of observable metric"""
        return self.name, self.value

    def cleanup(self):
        """Reset value"""
        if self.value:
            self.value = None

    def stop_collect(self):
        """Stop observe metric"""
        if self._active:
            self._active = False
        else:
            raise MetricCollectorIsStoppedError

    def __repr__(self):
        return f"MetricCollector(name={self.name}, " \
               f"target_function={self.target_function.__name__}, active={self._active})"


@functools.total_ordering
class Size:
    """Class to handle file size and pretty print it"""

    pow_map = OrderedDict(
        {
            1024 ** pw: letter
            for pw, letter in enumerate(["B", "K", "M", "G", "T", "P", "E", "Z", "Y"])
        }
    )

    def __init__(self, byte_len, pretty=False):
        self.len = byte_len
        self.pretty = pretty

    def __repr__(self):
        if not self.pretty:
            return f"{self.len}"
        else:
            for i, k in enumerate(Size.pow_map.keys()):
                if self.len == 0:
                    return f"{self.len}B"
                elif 1024 ** i < self.len < 1024 ** (i + 1):
                    return f"{self.len/k:.2f}{Size.pow_map[k]}"
                else:
                    continue

            raise ValueError(
                "Too large file. Consider using another program instead of this one."
            )

    def __str__(self):
        return self.__repr__()

    def __format__(self, format_spec):
        return f"{self.__repr__(): >7}"

    def __lt__(self, other):
        return self.len < other.len

    def __eq__(self, other):
        return self.len == other.len
