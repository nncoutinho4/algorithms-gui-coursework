"""Merge sort (divide and conquer) from scratch."""

from __future__ import annotations

from typing import List


def merge_sort(arr: List[int], ascending: bool = True) -> List[int]:
    a = arr[:]
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid], ascending=ascending)
    right = merge_sort(a[mid:], ascending=ascending)
    return _merge(left, right, ascending=ascending)


def _merge(left: List[int], right: List[int], ascending: bool) -> List[int]:
    merged: List[int] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if ascending:
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        else:
            if left[i] >= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged
