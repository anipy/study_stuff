
from typing import List
from itertools import chain
from operator import add
import numpy as np


def unpack1(arr: List[List[int]]) -> List[int]:
    """Unpack nested list with list comprehension"""
    inner_arr = arr[:]
    return [i for arr_item in inner_arr for i in arr_item]


def unpack2(arr: List[List[int]]) -> List[int]:
    """Unpack nested list with loop and star expression"""
    inner_arr = arr[:]
    result_arr = []
    for i in inner_arr:
        result_arr = [*result_arr, *i]
    return result_arr


def unpack3(arr: List[List[int]]) -> List[int]:
    """Unpack nested list with itertools.chain"""
    inner_arr = arr[:]
    return list(chain.from_iterable(inner_arr))


def unpack4(arr: List[List[int]]) -> List[int]:
    """Unpack nested list with pop() method"""
    inner_arr = arr[:]
    result_arr = []
    while inner_arr:
        result_arr.extend(inner_arr.pop(0))
    return result_arr


def unpack_benchmark(item_count: int = 10):
    """Demo functions caller"""
    arr = list(np.random.randint(100, size=(item_count, item_count)))
    arr = list(map(list, arr))
    
    unpack1(arr)
    unpack2(arr)
    unpack3(arr)
    unpack4(arr)
