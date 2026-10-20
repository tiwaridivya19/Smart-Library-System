
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from algorithms.stack_queue import Stack, Queue, Deque, PriorityQueue


class TestStack(unittest.TestCase):

    def setUp(self):
        self.stack = Stack()

    def test_push_and_pop(self):
        self.stack.push("Add Book")
        self.stack.push("Borrow Book")

        self.assertEqual(self.stack.pop(), "Borrow Book")
        self.assertEqual(self.stack.pop(), "Add Book")

    def test_peek(self):
        self.stack.push("Add Book")
        self.stack.push("Borrow Book")

        self.assertEqual(self.stack.peek(), "Borrow Book")
        self.assertEqual(self.stack.peek(), "Borrow Book")


class TestQueue(unittest.TestCase):

    def setUp(self):
        self.queue = Queue()

    def test_enqueue_and_dequeue(self):
        self.queue.enqueue("Request A")
        self.queue.enqueue("Request B")

        self.assertEqual(self.queue.dequeue(), "Request A")
        self.assertEqual(self.queue.dequeue(), "Request B")


class TestDeque(unittest.TestCase):

    def setUp(self):
        self.deque = Deque()

    def test_add_and_remove_from_both_ends(self):
        self.deque.add_front("A")
        self.deque.add_rear("B")

        self.assertEqual(self.deque.remove_front(), "A")
        self.assertEqual(self.deque.remove_rear(), "B")


class TestPriorityQueue(unittest.TestCase):

    def setUp(self):
        self.pq = PriorityQueue()

    def test_priority_order(self):
        self.pq.enqueue("Normal Request", 3)
        self.pq.enqueue("Urgent Request", 1)

        self.assertEqual(
            self.pq.dequeue(),
            (1, "Urgent Request")
        )
        self.assertEqual(
            self.pq.dequeue(),
            (3, "Normal Request")
        )


if __name__ == "__main__":
    unittest.main()
