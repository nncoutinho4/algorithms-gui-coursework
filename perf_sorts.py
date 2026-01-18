import random
import time

from algorithms.bubble_sort import bubble_sort
from algorithms.selection_sort import selection_sort
from algorithms.merge_sort import merge_sort


def time_it(fn, data):
    start = time.perf_counter()
    fn(data)
    end = time.perf_counter()
    return end - start


def main():
    sizes = [50, 200, 800]
    for n in sizes:
        data = [random.randint(0, 10000) for _ in range(n)]
        print(f"\nN={n}")
        print("Selection sort:", time_it(selection_sort, data))
        print("Bubble sort:", time_it(bubble_sort, data))
        print("Merge sort:", time_it(merge_sort, data))


if __name__ == "__main__":
    main()
