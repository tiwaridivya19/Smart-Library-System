
import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from algorithms.balanced_trees import BTree, BPlusTree


class TestBTree(unittest.TestCase):

    def setUp(self):
        self.btree = BTree(degree=3)

        for number in [10, 20, 5, 6, 12, 30, 7, 17, 25, 40, 50]:
            self.btree.insert(number)

    def test_search_existing_value(self):
        self.assertTrue(self.btree.search(17))

    def test_search_missing_value(self):
        self.assertFalse(self.btree.search(99))

    def test_traverse_sorted_values(self):
        self.assertEqual(
            self.btree.traverse(),
            [5, 6, 7, 10, 12, 17, 20, 25, 30, 40, 50]
        )


class TestBPlusTree(unittest.TestCase):

    def setUp(self):
        self.bplus = BPlusTree(order=4)

        for number in [10, 20, 5, 6, 12, 30, 7, 17, 25, 40, 50]:
            self.bplus.insert(number)

    def test_search_existing_value(self):
        self.assertTrue(self.bplus.search(17))

    def test_search_missing_value(self):
        self.assertFalse(self.bplus.search(99))

    def test_range_search(self):
        self.assertEqual(
            self.bplus.range_search(10, 30),
            [10, 12, 17, 20, 25, 30]
        )


if __name__ == "__main__":
    unittest.main()
