"""Count palindromic substrings using memoization (dynamic programming)."""

from __future__ import annotations

from typing import Dict, Tuple


def count_palindrome_substrings(s: str) -> int:
    n = len(s)
    memo: Dict[Tuple[int, int], bool] = {}

    def is_pal(i: int, j: int) -> bool:
        if i >= j:
            return True
        key = (i, j)
        if key in memo:
            return memo[key]
        if s[i] != s[j]:
            memo[key] = False
            return False
        memo[key] = is_pal(i + 1, j - 1)
        return memo[key]

    count = 0
    for i in range(n):
        for j in range(i, n):
            if is_pal(i, j):
                count += 1
    return count
