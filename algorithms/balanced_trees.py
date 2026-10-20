
class BTreeNode:
    def __init__(self, leaf=False):
        self.keys = []
        self.children = []
        self.leaf = leaf


class BTree:
    def __init__(self, degree=3):
        self.root = BTreeNode(leaf=True)
        self.degree = degree

    def search(self, key, node=None):
        if node is None:
            node = self.root

        i = 0

        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return True

        if node.leaf:
            return False

        return self.search(key, node.children[i])

    def insert(self, key):
        root = self.root

        if len(root.keys) == 2 * self.degree - 1:
            new_root = BTreeNode()
            new_root.children.append(root)
            self.root = new_root
            self._split_child(new_root, 0)
            self._insert_non_full(new_root, key)
        else:
            self._insert_non_full(root, key)

    def _split_child(self, parent, index):
        degree = self.degree
        full_child = parent.children[index]
        new_child = BTreeNode(leaf=full_child.leaf)

        middle_key = full_child.keys[degree - 1]

        new_child.keys = full_child.keys[degree:]
        full_child.keys = full_child.keys[:degree - 1]

        if not full_child.leaf:
            new_child.children = full_child.children[degree:]
            full_child.children = full_child.children[:degree]

        parent.children.insert(index + 1, new_child)
        parent.keys.insert(index, middle_key)

    def _insert_non_full(self, node, key):
        i = len(node.keys) - 1

        if node.leaf:
            if key in node.keys:
                return

            node.keys.append(key)

            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1

            node.keys[i + 1] = key
            return

        while i >= 0 and key < node.keys[i]:
            i -= 1

        i += 1

        if key in node.keys:
            return

        if len(node.children[i].keys) == 2 * self.degree - 1:
            self._split_child(node, i)

            if key > node.keys[i]:
                i += 1
            elif key == node.keys[i]:
                return

        self._insert_non_full(node.children[i], key)

    def traverse(self):
        result = []

        def visit(node):
            for i, key in enumerate(node.keys):
                if not node.leaf:
                    visit(node.children[i])

                result.append(key)

            if not node.leaf:
                visit(node.children[len(node.keys)])

        visit(self.root)
        return result


class BPlusNode:
    def __init__(self, leaf=False):
        self.keys = []
        self.children = []
        self.leaf = leaf
        self.next = None


class BPlusTree:
    def __init__(self, order=4):
        self.root = BPlusNode(leaf=True)
        self.order = order

    def search(self, key):
        node = self.root

        while not node.leaf:
            i = 0

            while i < len(node.keys) and key >= node.keys[i]:
                i += 1

            node = node.children[i]

        return key in node.keys

    def insert(self, key):
        result = self._insert(self.root, key)

        if result is not None:
            separator, right_node = result
            new_root = BPlusNode()
            new_root.keys = [separator]
            new_root.children = [self.root, right_node]
            self.root = new_root

    def _insert(self, node, key):
        if node.leaf:
            if key in node.keys:
                return None

            node.keys.append(key)
            node.keys.sort()

            if len(node.keys) < self.order:
                return None

            middle = len(node.keys) // 2
            right_node = BPlusNode(leaf=True)
            right_node.keys = node.keys[middle:]
            node.keys = node.keys[:middle]

            right_node.next = node.next
            node.next = right_node

            return right_node.keys[0], right_node

        i = 0

        while i < len(node.keys) and key >= node.keys[i]:
            i += 1

        result = self._insert(node.children[i], key)

        if result is None:
            return None

        separator, right_node = result
        node.keys.insert(i, separator)
        node.children.insert(i + 1, right_node)

        if len(node.keys) < self.order:
            return None

        middle = len(node.keys) // 2
        promoted_key = node.keys[middle]

        new_right = BPlusNode()
        new_right.keys = node.keys[middle + 1:]
        new_right.children = node.children[middle + 1:]

        node.keys = node.keys[:middle]
        node.children = node.children[:middle + 1]

        return promoted_key, new_right

    def range_search(self, start, end):
        node = self.root

        while not node.leaf:
            i = 0

            while i < len(node.keys) and start >= node.keys[i]:
                i += 1

            node = node.children[i]

        result = []

        while node is not None:
            for key in node.keys:
                if start <= key <= end:
                    result.append(key)

                if key > end:
                    return result

            node = node.next

        return result
