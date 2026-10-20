
import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from algorithms.dsu import DisjointSet


class TestDisjointSet(unittest.TestCase):

    def setUp(self):
        self.dsu = DisjointSet([1, 2, 3, 4, 5, 6])

    def test_union_operations(self):
        self.assertTrue(self.dsu.union(1, 2))
        self.assertTrue(self.dsu.union(2, 3))
        self.assertTrue(self.dsu.union(4, 5))

    def test_connectivity(self):
        self.dsu.union(1, 2)
        self.dsu.union(2, 3)
        self.dsu.union(4, 5)

        self.assertTrue(self.dsu.connected(1, 3))
        self.assertFalse(self.dsu.connected(1, 4))
        self.assertTrue(self.dsu.connected(4, 5))

    def test_duplicate_union(self):
        self.dsu.union(1, 2)
        self.dsu.union(2, 3)

        self.assertFalse(self.dsu.union(1, 3))

    def test_join_two_groups(self):
        self.dsu.union(1, 2)
        self.dsu.union(2, 3)
        self.dsu.union(4, 5)

        self.assertTrue(self.dsu.union(3, 4))
        self.assertTrue(self.dsu.connected(1, 5))

    def test_get_sets(self):
        self.dsu.union(1, 2)
        self.dsu.union(2, 3)
        self.dsu.union(4, 5)

        groups = self.dsu.get_sets()

        actual_groups = {
            frozenset(group)
            for group in groups
        }

        expected_groups = {
            frozenset({1, 2, 3}),
            frozenset({4, 5}),
            frozenset({6})
        }

        self.assertEqual(len(groups), 3)
        self.assertEqual(actual_groups, expected_groups)

    def test_unknown_element(self):
        with self.assertRaises(KeyError):
            self.dsu.find(99)


if __name__ == "__main__":
    unittest.main()
