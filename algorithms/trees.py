
class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


class BinarySearchTree:
    def __init__(self):
        self.root = None

    def insert(self, data):
        if self.root is None:
            self.root = TreeNode(data)
            return

        current = self.root

        while True:
            if data < current.data:
                if current.left is None:
                    current.left = TreeNode(data)
                    return
                current = current.left

            elif data > current.data:
                if current.right is None:
                    current.right = TreeNode(data)
                    return
                current = current.right

            else:
                return

    def search(self, data):
        current = self.root

        while current is not None:
            if data == current.data:
                return True
            elif data < current.data:
                current = current.left
            else:
                current = current.right

        return False

    def inorder(self):
        result = []

        def traverse(node):
            if node is not None:
                traverse(node.left)
                result.append(node.data)
                traverse(node.right)

        traverse(self.root)
        return result

    def preorder(self):
        result = []

        def traverse(node):
            if node is not None:
                result.append(node.data)
                traverse(node.left)
                traverse(node.right)

        traverse(self.root)
        return result

    def postorder(self):
        result = []

        def traverse(node):
            if node is not None:
                traverse(node.left)
                traverse(node.right)
                result.append(node.data)

        traverse(self.root)
        return result

    def delete(self, data):
        self.root = self._delete_node(self.root, data)

    def _delete_node(self, node, data):
        if node is None:
            return None

        if data < node.data:
            node.left = self._delete_node(node.left, data)

        elif data > node.data:
            node.right = self._delete_node(node.right, data)

        else:
            if node.left is None:
                return node.right

            if node.right is None:
                return node.left

            successor = node.right

            while successor.left is not None:
                successor = successor.left

            node.data = successor.data
            node.right = self._delete_node(
                node.right, successor.data
            )

        return node

class AVLNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def height(self, node):
        if node is None:
            return 0
        return node.height

    def balance_factor(self, node):
        if node is None:
            return 0

        return self.height(node.left) - self.height(node.right)

    def rotate_right(self, y):
        x = y.left
        temp = x.right

        x.right = y
        y.left = temp

        y.height = 1 + max(
            self.height(y.left),
            self.height(y.right)
        )

        x.height = 1 + max(
            self.height(x.left),
            self.height(x.right)
        )

        return x

    def rotate_left(self, x):
        y = x.right
        temp = y.left

        y.left = x
        x.right = temp

        x.height = 1 + max(
            self.height(x.left),
            self.height(x.right)
        )

        y.height = 1 + max(
            self.height(y.left),
            self.height(y.right)
        )

        return y

    def insert(self, data):
        self.root = self._insert(self.root, data)

    def _insert(self, node, data):
        if node is None:
            return AVLNode(data)

        if data < node.data:
            node.left = self._insert(node.left, data)
        elif data > node.data:
            node.right = self._insert(node.right, data)
        else:
            return node

        node.height = 1 + max(
            self.height(node.left),
            self.height(node.right)
        )

        balance = self.balance_factor(node)

        # Left-Left case
        if balance > 1 and data < node.left.data:
            return self.rotate_right(node)

        # Right-Right case
        if balance < -1 and data > node.right.data:
            return self.rotate_left(node)

        # Left-Right case
        if balance > 1 and data > node.left.data:
            node.left = self.rotate_left(node.left)
            return self.rotate_right(node)

        # Right-Left case
        if balance < -1 and data < node.right.data:
            node.right = self.rotate_right(node.right)
            return self.rotate_left(node)

        return node

    def search(self, data):
        current = self.root

        while current is not None:
            if data == current.data:
                return True
            elif data < current.data:
                current = current.left
            else:
                current = current.right

        return False

    def inorder(self):
        result = []

        def traverse(node):
            if node is not None:
                traverse(node.left)
                result.append(node.data)
                traverse(node.right)

        traverse(self.root)
        return result
