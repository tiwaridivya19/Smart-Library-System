
import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from algorithms.trees import BinarySearchTree, AVLTree


class TestBinarySearchTree(unittest.TestCase):

    def setUp(self):
        self.tree = BinarySearchTree()

        for number in [50, 30, 70, 20, 40, 60, 80]:
            self.tree.insert(number)

    def test_search_existing_value(self):
        self.assertTrue(self.tree.search(40))

    def test_search_missing_value(self):
        self.assertFalse(self.tree.search(90))

    def test_inorder_traversal(self):
        self.assertEqual(
            self.tree.inorder(),
            [20, 30, 40, 50, 60, 70, 80]
        )

    def test_preorder_traversal(self):
        self.assertEqual(
            self.tree.preorder(),
            [50, 30, 20, 40, 70, 60, 80]
        )

    def test_postorder_traversal(self):
        self.assertEqual(
            self.tree.postorder(),
            [20, 40, 30, 60, 80, 70, 50]
        )

    def test_delete_leaf_node(self):
        self.tree.delete(20)

        self.assertEqual(
            self.tree.inorder(),
            [30, 40, 50, 60, 70, 80]
        )

    def test_delete_node_with_one_child_or_leaf(self):
        self.tree.delete(20)
        self.tree.delete(30)

        self.assertEqual(
            self.tree.inorder(),
            [40, 50, 60, 70, 80]
        )

    def test_delete_node_with_two_children(self):
        self.tree.delete(50)

        self.assertEqual(
            self.tree.inorder(),
            [20, 30, 40, 60, 70, 80]
        )


class TestAVLTree(unittest.TestCase):

    def test_left_left_rotation(self):
        avl = AVLTree()

        for number in [30, 20, 10]:
            avl.insert(number)

        self.assertEqual(avl.root.data, 20)
        self.assertEqual(avl.inorder(), [10, 20, 30])

    def test_right_right_rotation(self):
        avl = AVLTree()

        for number in [10, 20, 30]:
            avl.insert(number)

        self.assertEqual(avl.root.data, 20)
        self.assertEqual(avl.inorder(), [10, 20, 30])

    def test_left_right_rotation(self):
        avl = AVLTree()

        for number in [30, 10, 20]:
            avl.insert(number)

        self.assertEqual(avl.root.data, 20)
        self.assertEqual(avl.inorder(), [10, 20, 30])

    def test_right_left_rotation(self):
        avl = AVLTree()

        for number in [10, 30, 20]:
            avl.insert(number)

        self.assertEqual(avl.root.data, 20)
        self.assertEqual(avl.inorder(), [10, 20, 30])

    def test_search(self):
        avl = AVLTree()

        for number in [10, 30, 20]:
            avl.insert(number)

        self.assertTrue(avl.search(20))
        self.assertFalse(avl.search(99))


if __name__ == "__main__":
    unittest.main()
