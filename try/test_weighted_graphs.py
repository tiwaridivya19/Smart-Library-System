
import sys
import os
import unittest

sys.path.insert(
    0,
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

from algorithms.graphs import WeightedGraph


class TestWeightedGraphMST(unittest.TestCase):

    def setUp(self):
        self.graph = WeightedGraph()

        self.graph.add_edge("A", "B", 1)
        self.graph.add_edge("A", "C", 4)
        self.graph.add_edge("B", "C", 2)
        self.graph.add_edge("B", "D", 5)
        self.graph.add_edge("C", "D", 3)

    def test_prim_mst_edge_count(self):
        prim_edges, prim_weight = self.graph.prim_mst("A")

        self.assertEqual(len(prim_edges), 3)

    def test_prim_mst_total_weight(self):
        prim_edges, prim_weight = self.graph.prim_mst("A")

        self.assertEqual(prim_weight, 6)

    def test_kruskal_mst_edge_count(self):
        kruskal_edges, kruskal_weight = self.graph.kruskal_mst()

        self.assertEqual(len(kruskal_edges), 3)

    def test_kruskal_mst_total_weight(self):
        kruskal_edges, kruskal_weight = self.graph.kruskal_mst()

        self.assertEqual(kruskal_weight, 6)

    def test_prim_and_kruskal_total_weights_match(self):
        _, prim_weight = self.graph.prim_mst("A")
        _, kruskal_weight = self.graph.kruskal_mst()

        self.assertEqual(prim_weight, kruskal_weight)

    def test_empty_graph(self):
        empty_graph = WeightedGraph()

        self.assertEqual(empty_graph.prim_mst("A"), ([], 0))
        self.assertEqual(empty_graph.kruskal_mst(), ([], 0))

    def test_disconnected_graph(self):
        disconnected_graph = WeightedGraph()
        disconnected_graph.add_edge("A", "B", 2)
        disconnected_graph.add_vertex("C")

        self.assertEqual(
            disconnected_graph.prim_mst("A"),
            ([], 0)
        )
        self.assertEqual(
            disconnected_graph.kruskal_mst(),
            ([], 0)
        )


if __name__ == "__main__":
    unittest.main()
