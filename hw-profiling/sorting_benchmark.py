
from typing import List
from random import sample


def bubble_sort(arr: List[int]) -> List[int]:
    """Implementation of bubble sort algorithm"""
    n = len(arr)

    for i in range(n):
        is_sorted = True
        for j in range(n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                is_sorted = False
        if is_sorted:
            break

    return arr


def tim_sort(arr: List[int]) -> List[int]:
    """Default python sorting"""   
    return sorted(arr)


def insertion_sort(arr: List[int]) -> List[int]:
    """Implementation of bubble sort algorithm"""
    for i in range(1, len(arr)):
        k = arr[i]
        j = i - 1        
        while j >= 0 and arr[j] > k:
            arr[j + 1] = arr[j]
            j -= 1            
        arr[j + 1] = k
    return arr


def sorting_benchmark(arange=10):
    """Demo functions launcher"""
    arr = sample(range(arange), arange)
    
    bubble_sort(arr)
    insertion_sort(arr)
    tim_sort(arr)
