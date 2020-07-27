"""Helper classes for ls utility"""

from collections import OrderedDict
import functools


class EntryInfo:
    """Class to store entries information and provide printable representation for it"""
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return '  '.join(f'{k}: {v}' for k, v in self.__dict__.items())

    def build_printable(self,
                        pretty_size: bool = False,
                        show_time: str = 'ctime',
                        long_format: bool = False):
        """Depending on required format returns EntryInfo representation

        Args:
          pretty_size: set up human-readable format for file size if True,
            otherwise set up raw format in bytes

          show_time: set up what time to show. One of (`atime`, `ctime`, `mtime`)

          long_format: set up full format (time, mode, size, name) if True,
            otherwise set up short format (name)
        """

        if show_time not in ('atime', 'ctime', 'mtime'):
            raise ValueError('Only (`atime`, `ctime`, `mtime`) allowed for show_time argument')

        if not long_format:
            return self.__dict__.get('name')

        return '  '.join(
            [
                self.__dict__.get(show_time),
                self.__dict__.get('mode'),
                f"{str(self.__dict__.get('size_pretty' if pretty_size else 'size'))}",
                self.__dict__.get('name')
            ]
        )


@functools.total_ordering
class Size:
    """Class to handle file size and pretty print it"""
    pow_map = OrderedDict({
        1024 ** pw: letter for pw, letter in enumerate([
            'B', 'K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'
        ])
    })

    def __init__(self, byte_len, pretty=False):
        self.len = byte_len
        self.pretty = pretty

    def __repr__(self):
        if not self.pretty:
            return f'{self.len}'
        else:
            for i, k in enumerate(Size.pow_map.keys()):
                if self.len == 0:
                    return f'{self.len}B'
                elif 1024 ** i < self.len < 1024 ** (i+1):
                    return f'{self.len/k:.2f}{Size.pow_map[k]}'
                else:
                    continue

            raise ValueError('Too large file. Consider using another program instead of this one.')

    def __str__(self):
        return self.__repr__()

    def __format__(self, format_spec):
        return f'{self.__repr__(): >7}'

    def __lt__(self, other):
        return self.len < other.len

    def __eq__(self, other):
        return self.len == other.len
