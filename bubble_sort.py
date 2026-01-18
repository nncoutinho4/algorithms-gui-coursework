"""Bubble sort from scratch."""

from __future__ import annotations

from typing import List


def bubble_sort(arr: List[int], ascending: bool = True) -> List[int]:
    a = arr[:]  # do not mutate input
    n = len(a)
    for i in range(n):
        swapped = False
        for j in range(0, n - 1 - i):
            if ascending:
                if a[j] > a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    swapped = True
            else:
                if a[j] < a[j + 1]:
                    a[j], a[j + 1] = a[j + 1], a[j]
                    swapped = True
        if not swapped:
            break
    return a
