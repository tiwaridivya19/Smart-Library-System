
class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [[] for _ in range(size)]

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        bucket = self.table[index]

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket[i] = (key, value)
                return

        bucket.append((key, value))

    def search(self, key):
        index = self._hash(key)

        for stored_key, value in self.table[index]:
            if stored_key == key:
                return value

        return None

    def delete(self, key):
        index = self._hash(key)
        bucket = self.table[index]

        for i in range(len(bucket)):
            if bucket[i][0] == key:
                bucket.pop(i)
                return True

        return False

    def display(self):
        return self.table
