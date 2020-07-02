
from typing import Dict, List, Any


def to_upper1(words: List[str]) -> List[str]:
    """Apply uppercase on each string in a list with list comprehension """
    return [w.upper() for w in words]


def to_upper2(words: List[str]) -> List[str]:
    """Apply uppercase on each string in a list with map function"""
    return list(map(str.upper, words))


def to_power1(arr: List[int], power: int = 2) -> List[int]:
    """Set power for each number in a list using pow operator `**`"""
    return [x**power for x in arr]


def to_power2(arr: List[int], power: int = 2) -> List[int]:
    """Set power for each number in a list using magic method __pow__()"""
    return [x.__pow__(power) for x in arr]


def to_power3(arr: List[int], power: int = 2) -> List[int]:
    """Set power for each number in a list using list constructor and builtin function pow()"""
    return list(map(lambda x: pow(x, power), arr))


def list_benchmark():
    """Function for demonstration purposes"""
    
    tokens = ['foo', 'bar', 'sPaM', 'EggS'] * 1_000_000
    arr = list(range(1_000_000))
    
    to_upper1(tokens)
    to_upper2(tokens)
    
    to_power1(arr)
    to_power2(arr)
    to_power3(arr)
