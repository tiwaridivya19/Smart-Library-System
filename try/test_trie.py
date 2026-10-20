
import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from algorithms.trie import Trie


class TestTrie(unittest.TestCase):

    def setUp(self):
        self.trie = Trie()

        self.books = [
            "Python",
            "Physics",
            "Philosophy",
            "Data",
            "Database"
        ]

        for word in self.books:
            self.trie.insert(word)

    def test_search_existing_words(self):
        self.assertTrue(self.trie.search("Python"))
        self.assertTrue(self.trie.search("Physics"))

    def test_search_is_case_insensitive(self):
        self.assertTrue(self.trie.search("python"))

    def test_search_prefix_is_not_full_word(self):
        self.assertFalse(self.trie.search("Py"))

    def test_search_unknown_word(self):
        self.assertFalse(self.trie.search("Unknown"))

    def test_starts_with_existing_prefixes(self):
        self.assertTrue(self.trie.starts_with("Phy"))
        self.assertTrue(self.trie.starts_with("Phi"))
        self.assertTrue(self.trie.starts_with("Dat"))

    def test_starts_with_unknown_prefix(self):
        self.assertFalse(self.trie.starts_with("xyz"))

    def test_autocomplete_phy(self):
        self.assertEqual(
            self.trie.autocomplete("Phy"),
            ["physics"]
        )

    def test_autocomplete_phi(self):
        self.assertEqual(
            self.trie.autocomplete("Phi"),
            ["philosophy"]
        )

    def test_autocomplete_data(self):
        self.assertEqual(
            self.trie.autocomplete("Data"),
            ["data", "database"]
        )

    def test_autocomplete_py(self):
        self.assertEqual(
            self.trie.autocomplete("Py"),
            ["python"]
        )

    def test_autocomplete_unknown_prefix(self):
        self.assertEqual(
            self.trie.autocomplete("xyz"),
            []
        )


if __name__ == "__main__":
    unittest.main()
