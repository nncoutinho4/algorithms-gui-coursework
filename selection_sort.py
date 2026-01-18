"""Selection sort from scratch."""

from __future__ import annotations

from typing import List


def selection_sort(arr: List[int], ascending: bool = True) -> List[int]:
    a = arr[:]  # do not mutate input
    n = len(a)
    for i in range(n):
        best_idx = i
        for j in range(i + 1, n):
            if ascending:
                if a[j] < a[best_idx]:
                    best_idx = j
            else:
                if a[j] > a[best_idx]:
                    best_idx = j
        a[i], a[best_idx] = a[best_idx], a[i]
    return a
