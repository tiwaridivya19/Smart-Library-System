
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def add(self, data):
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
            return

        current = self.head

        while current.next is not None:
            current = current.next

        current.next = new_node

    def add_front(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def display(self):
        activities = []
        current = self.head

        while current is not None:
            activities.append(current.data)
            current = current.next

        return activities

    def delete(self, data):
        if self.head is None:
            return False

        if self.head.data == data:
            self.head = self.head.next
            return True

        current = self.head

        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next
                return True

            current = current.next

        return False
