
import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from algorithms.searching_sorting import (
    linear_search,
    binary_search,
    bubble_sort,
    merge_sort,
    quick_sort
)


class TestSearchingSorting(unittest.TestCase):

    def setUp(self):
        self.numbers = [12, 5, 18, 2, 9]
        self.sorted_numbers = [2, 5, 9, 12, 18]

    def test_linear_search_found(self):
        self.assertEqual(linear_search(self.numbers, 18), 2)

    def test_linear_search_not_found(self):
        self.assertEqual(linear_search(self.numbers, 99), -1)

    def test_binary_search_found(self):
        self.assertEqual(binary_search(self.sorted_numbers, 12), 3)

    def test_binary_search_not_found(self):
        self.assertEqual(binary_search(self.sorted_numbers, 99), -1)

    def test_bubble_sort(self):
        self.assertEqual(bubble_sort(self.numbers), self.sorted_numbers)

    def test_merge_sort(self):
        self.assertEqual(merge_sort(self.numbers), self.sorted_numbers)

    def test_quick_sort(self):
        self.assertEqual(quick_sort(self.numbers), self.sorted_numbers)

    def test_merge_sort_empty_list(self):
        self.assertEqual(merge_sort([]), [])

    def test_quick_sort_single_element(self):
        self.assertEqual(quick_sort([5]), [5])

    def test_bubble_sort_duplicates(self):
        self.assertEqual(bubble_sort([3, 3, 1]), [1, 3, 3])


if __name__ == "__main__":
    unittest.main()
