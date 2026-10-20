
import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from algorithms.hashing import HashTable


class TestHashTable(unittest.TestCase):

    def setUp(self):
        self.table = HashTable(size=5)

    def test_insert_and_search(self):
        self.table.insert("Python", "Programming")
        self.table.insert("DSA", "Data Structures")

        self.assertEqual(
            self.table.search("Python"),
            "Programming"
        )
        self.assertEqual(
            self.table.search("DSA"),
            "Data Structures"
        )

    def test_update_existing_key(self):
        self.table.insert("Python", "Programming")
        self.table.insert("Python", "Updated Programming")

        self.assertEqual(
            self.table.search("Python"),
            "Updated Programming"
        )

    def test_search_unknown_key(self):
        self.assertIsNone(self.table.search("Unknown"))

    def test_delete_existing_key(self):
        self.table.insert("DSA", "Data Structures")

        self.assertTrue(self.table.delete("DSA"))
        self.assertIsNone(self.table.search("DSA"))

    def test_delete_unknown_key(self):
        self.assertFalse(self.table.delete("Unknown"))


if __name__ == "__main__":
    unittest.main()
