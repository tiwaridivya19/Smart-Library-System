
class DisjointSet:
    def __init__(self, elements):
        self.parent = {}
        self.rank = {}

        for element in elements:
            self.parent[element] = element
            self.rank[element] = 0

    def find(self, element):
        if element not in self.parent:
            raise KeyError(f"Unknown element: {element}")

        if self.parent[element] != element:
            self.parent[element] = self.find(
                self.parent[element]
            )

        return self.parent[element]

    def union(self, element1, element2):
        root1 = self.find(element1)
        root2 = self.find(element2)

        if root1 == root2:
            return False

        if self.rank[root1] < self.rank[root2]:
            self.parent[root1] = root2

        elif self.rank[root1] > self.rank[root2]:
            self.parent[root2] = root1

        else:
            self.parent[root2] = root1
            self.rank[root1] += 1

        return True

    def connected(self, element1, element2):
        return self.find(element1) == self.find(element2)

    def get_sets(self):
        groups = {}

        for element in self.parent:
            root = self.find(element)

            if root not in groups:
                groups[root] = []

            groups[root].append(element)

        return list(groups.values())
