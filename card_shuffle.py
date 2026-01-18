"""Randomised algorithm: Fisher-Yates shuffle on a standard 52-card deck."""

from __future__ import annotations

import random
from typing import List


def create_standard_deck() -> List[str]:
    suits = ["S", "H", "D", "C"]
    ranks = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    deck: List[str] = []
    for s in suits:
        for r in ranks:
            deck.append(f"{r}{s}")
    return deck


def fisher_yates_shuffle(deck: List[str], seed: int | None = None) -> List[str]:
    if seed is not None:
        random.seed(seed)
    a = deck[:]
    for i in range(len(a) - 1, 0, -1):
        j = random.randint(0, i)
        a[i], a[j] = a[j], a[i]
    return a
