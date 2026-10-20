
import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from algorithms.graphs import Graph


class TestGraphs(unittest.TestCase):

    def setUp(self):
        self.graph = Graph()

        self.graph.add_edge("A", "B")
        self.graph.add_edge("A", "C")
        self.graph.add_edge("B", "D")
        self.graph.add_edge("C", "D")

    def test_bfs(self):
        self.assertEqual(
            self.graph.bfs("A"),
            ["A", "B", "C", "D"]
        )

    def test_dfs(self):
        self.assertEqual(
            self.graph.dfs("A"),
            ["A", "B", "D", "C"]
        )

    def test_bfs_missing_vertex(self):
        self.assertEqual(self.graph.bfs("X"), [])

    def test_dfs_missing_vertex(self):
        self.assertEqual(self.graph.dfs("X"), [])

    def test_add_vertex(self):
        self.graph.add_vertex("E")

        self.assertIn("E", self.graph.adjacency_list)
        self.assertEqual(self.graph.adjacency_list["E"], [])

    def test_add_edge(self):
        self.assertIn("B", self.graph.adjacency_list["A"])
        self.assertIn("A", self.graph.adjacency_list["B"])

    def test_connected_components(self):
        self.graph.add_vertex("E")
        self.graph.add_edge("F", "G")

        components = self.graph.connected_components()

        actual_components = {
            frozenset(component)
            for component in components
        }

        expected_components = {
            frozenset({"A", "B", "C", "D"}),
            frozenset({"E"}),
            frozenset({"F", "G"})
        }

        self.assertEqual(len(components), 3)
        self.assertEqual(actual_components, expected_components)


if __name__ == "__main__":
    unittest.main()
