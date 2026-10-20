
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from algorithms.linked_list import LinkedList
from algorithms.hashing import HashTable
from algorithms.searching_sorting import merge_sort
from algorithms.trie import Trie
from algorithms.trees import BinarySearchTree
from algorithms.stack_queue import Stack, Queue


class TestLibraryAlgorithms(unittest.TestCase):

    def test_book_title_sorting(self):
        titles = ["The Hobbit", "Atomic Habits", "Python"]
        self.assertEqual(
            merge_sort(titles),
            ["Atomic Habits", "Python", "The Hobbit"]
        )

    def test_book_hash_lookup(self):
        table = HashTable(size=5)
        table.insert("B001", "Harry Potter")
        table.insert("B002", "The Hobbit")

        self.assertEqual(table.search("B001"), "Harry Potter")
        self.assertEqual(table.search("B002"), "The Hobbit")

    def test_book_title_autocomplete(self):
        trie = Trie()
        trie.insert("Harry Potter")
        trie.insert("Harry Potter and the Chamber of Secrets")
        trie.insert("The Hobbit")

        self.assertEqual(
            trie.autocomplete("Harry"),
            [
                "harry potter",
                "harry potter and the chamber of secrets"
            ]
        )

    def test_bst_book_listing(self):
        tree = BinarySearchTree()

        for book_id in [103, 101, 105, 102, 104]:
            tree.insert(book_id)

        self.assertEqual(
            tree.inorder(),
            [101, 102, 103, 104, 105]
        )

    def test_activity_history(self):
        activities = LinkedList()
        activities.add("Added Harry Potter")
        activities.add("Borrowed The Hobbit")

        self.assertEqual(
            activities.display(),
            ["Added Harry Potter", "Borrowed The Hobbit"]
        )

    def test_request_queue_fifo(self):
        requests = Queue()
        requests.enqueue("Request A")
        requests.enqueue("Request B")

        self.assertEqual(requests.dequeue(), "Request A")
        self.assertEqual(requests.dequeue(), "Request B")

    def test_request_stack_lifo(self):
        requests = Stack()
        requests.push("Add Book")
        requests.push("Borrow Book")

        self.assertEqual(requests.pop(), "Borrow Book")
        self.assertEqual(requests.pop(), "Add Book")


if __name__ == "__main__":
    unittest.main()
