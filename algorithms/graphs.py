
from collections import deque


class Graph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, vertex1, vertex2):
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)

        if vertex2 not in self.adjacency_list[vertex1]:
            self.adjacency_list[vertex1].append(vertex2)

        if vertex1 not in self.adjacency_list[vertex2]:
            self.adjacency_list[vertex2].append(vertex1)

    def bfs(self, start):
        if start not in self.adjacency_list:
            return []

        visited = {start}
        result = []
        queue = deque([start])

        while queue:
            vertex = queue.popleft()
            result.append(vertex)

            for neighbor in self.adjacency_list[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return result

    def dfs(self, start):
        if start not in self.adjacency_list:
            return []

        visited = set()
        result = []

        def visit(vertex):
            visited.add(vertex)
            result.append(vertex)

            for neighbor in self.adjacency_list[vertex]:
                if neighbor not in visited:
                    visit(neighbor)

        visit(start)
        return result

    def connected_components(self):
        visited = set()
        components = []

        for vertex in self.adjacency_list:
            if vertex not in visited:
                component = []
                queue = deque([vertex])
                visited.add(vertex)

                while queue:
                    current = queue.popleft()
                    component.append(current)

                    for neighbor in self.adjacency_list[current]:
                        if neighbor not in visited:
                            visited.add(neighbor)
                            queue.append(neighbor)

                components.append(component)

        return components

    def display(self):
        return self.adjacency_list

class WeightedGraph:
    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []

    def add_edge(self, vertex1, vertex2, weight):
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)

        self.adjacency_list[vertex1].append((vertex2, weight))
        self.adjacency_list[vertex2].append((vertex1, weight))

    def prim_mst(self, start):
        import heapq

        if start not in self.adjacency_list:
            return [], 0

        visited = {start}
        edges = []
        mst = []
        total_weight = 0

        for neighbor, weight in self.adjacency_list[start]:
            heapq.heappush(
                edges, (weight, start, neighbor)
            )

        while edges and len(visited) < len(self.adjacency_list):
            weight, source, destination = heapq.heappop(edges)

            if destination in visited:
                continue

            visited.add(destination)
            mst.append((source, destination, weight))
            total_weight += weight

            for neighbor, next_weight in self.adjacency_list[destination]:
                if neighbor not in visited:
                    heapq.heappush(
                        edges,
                        (next_weight, destination, neighbor)
                    )

        if len(visited) != len(self.adjacency_list):
            return [], 0

        return mst, total_weight

    def kruskal_mst(self):
        parent = {
            vertex: vertex for vertex in self.adjacency_list
        }
        rank = {
            vertex: 0 for vertex in self.adjacency_list
        }

        def find(vertex):
            if parent[vertex] != vertex:
                parent[vertex] = find(parent[vertex])
            return parent[vertex]

        def union(vertex1, vertex2):
            root1 = find(vertex1)
            root2 = find(vertex2)

            if root1 == root2:
                return False

            if rank[root1] < rank[root2]:
                parent[root1] = root2
            elif rank[root1] > rank[root2]:
                parent[root2] = root1
            else:
                parent[root2] = root1
                rank[root1] += 1

            return True

        all_edges = []

        for vertex in self.adjacency_list:
            for neighbor, weight in self.adjacency_list[vertex]:
                if str(vertex) < str(neighbor):
                    all_edges.append(
                        (weight, vertex, neighbor)
                    )

        all_edges.sort()

        mst = []
        total_weight = 0

        for weight, vertex1, vertex2 in all_edges:
            if union(vertex1, vertex2):
                mst.append((vertex1, vertex2, weight))
                total_weight += weight

        if len(self.adjacency_list) > 0 and len(mst) != len(self.adjacency_list) - 1:
            return [], 0

        return mst, total_weight
