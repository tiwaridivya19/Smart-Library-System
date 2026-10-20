
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from algorithms.linked_list import LinkedList


class TestLinkedList(unittest.TestCase):

    def setUp(self):
        self.activities = LinkedList()

    def test_add_and_display(self):
        self.activities.add("Added Harry Potter")
        self.activities.add("Borrowed The Hobbit")
        self.activities.add("Returned The Hobbit")

        self.assertEqual(
            self.activities.display(),
            [
                "Added Harry Potter",
                "Borrowed The Hobbit",
                "Returned The Hobbit"
            ]
        )

    def test_delete_existing_activity(self):
        self.activities.add("Added Harry Potter")
        self.activities.add("Borrowed The Hobbit")
        self.activities.add("Returned The Hobbit")

        self.assertTrue(
            self.activities.delete("Borrowed The Hobbit")
        )

        self.assertEqual(
            self.activities.display(),
            [
                "Added Harry Potter",
                "Returned The Hobbit"
            ]
        )

    def test_delete_missing_activity(self):
        self.assertFalse(
            self.activities.delete("Missing Activity")
        )

    def test_delete_from_empty_list(self):
        self.assertFalse(
            self.activities.delete("Missing Activity")
        )
        self.assertEqual(self.activities.display(), [])


if __name__ == "__main__":
    unittest.main()
