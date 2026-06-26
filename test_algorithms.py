import random

from sorting_algorithms import insertion_sort, merge_sort
from benchmark_sorting import generate_data


def check_one_case(data):
    expected_answer = sorted(data)

    original_for_insertion = data.copy()
    original_for_merge = data.copy()

    insertion_answer = insertion_sort(original_for_insertion)#This is to sort the list using insertion sort. We pass in a copy of the original list so that we do not modify the original list. This is important because we want to check that the original list is not modified by the sorting algorithm.
    merge_answer = merge_sort(original_for_merge)#and this is the same thing but for merge sort.

    if insertion_answer != expected_answer:
        print("Insertion sort failed")
        print("Original data:", data)
        print("Expected:", expected_answer)
        print("Got:", insertion_answer)
        raise AssertionError

    if merge_answer != expected_answer:
        print("Merge sort failed")
        print("Original data:", data)
        print("Expected:", expected_answer)
        print("Got:", merge_answer)
        raise AssertionError

    if original_for_insertion != data:
        print("Insertion sort changed the original list")
        print("Before:", data)
        print("After:", original_for_insertion)
        raise AssertionError

    if original_for_merge != data:
        print("Merge sort changed the original list")
        print("Before:", data)
        print("After:", original_for_merge)
        raise AssertionError


def run_small_manual_tests():
    small_cases = [
        [],
        [1],
        [2, 1],
        [1, 2],
        [4, 4, 4, 4],
        [3, 1, 2, 3, 1],
        [0, -2, 7, 3, -1],
        [10, 5, 0, -5, 10],
        [9, 8, 7, 6, 5],
    ]

    for case in small_cases:
        check_one_case(case)


def run_generated_tests():
    random.seed(100)

    sizes_to_try = [0, 1, 2, 5, 10, 30, 75]

    data_types_to_try = [
        "random",
        "sorted",
        "reverse",
        "duplicates",
        "nearly_sorted",
        "all_equal",
        "few_unique",
    ]

    for data_type in data_types_to_try:
        for size in sizes_to_try:
            generated_list = generate_data(size, data_type)
            check_one_case(generated_list)


if __name__ == "__main__":
    run_small_manual_tests()
    run_generated_tests()

    print("All checks passed.")