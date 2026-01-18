"""Compute basic descriptive statistics from scratch.

Returns:
- smallest
- largest
- mode (may be multiple)
- median
- Q1 (1st quartile)
- Q3 (3rd quartile)

Quartiles use the Tukey method (median of lower and upper halves).
"""

from __future__ import annotations

from typing import Dict, List, Union

Number = Union[int, float]


def _median_sorted(values: List[Number]) -> Number:
    n = len(values)
    if n == 0:
        raise ValueError("array must not be empty")
    mid = n // 2
    if n % 2 == 1:
        return values[mid]
    return (values[mid - 1] + values[mid]) / 2


def describe(arr: List[Number]) -> Dict[str, object]:
    if not arr:
        raise ValueError("array must not be empty")

    smallest = largest = arr[0]
    for x in arr[1:]:
        if x < smallest:
            smallest = x
        if x > largest:
            largest = x

    freq: Dict[Number, int] = {}
    for x in arr:
        freq[x] = freq.get(x, 0) + 1
    max_count = max(freq.values())
    modes = sorted([k for k, v in freq.items() if v == max_count])

    sorted_vals = sorted(arr)
    med = _median_sorted(sorted_vals)

    n = len(sorted_vals)
    mid = n // 2
    if n % 2 == 0:
        lower = sorted_vals[:mid]
        upper = sorted_vals[mid:]
    else:
        lower = sorted_vals[:mid]
        upper = sorted_vals[mid + 1 :]

    q1 = _median_sorted(lower) if lower else sorted_vals[0]
    q3 = _median_sorted(upper) if upper else sorted_vals[-1]

    return {
        "smallest": smallest,
        "largest": largest,
        "mode": modes,
        "mode_count": max_count,
        "median": med,
        "q1": q1,
        "q3": q3,
        "sorted": sorted_vals,
    }
