# test_hierarchy_graph.py
import pytest
import networkx as nx
from unittest.mock import Mock, patch

from sourcemodel.herrarchy_graph import HierarchyGraph


@pytest.fixture
def sample_hierarchy_graph():
    return HierarchyGraph()


def test_initialization(sample_hierarchy_graph):
    assert isinstance(sample_hierarchy_graph.graph, nx.DiGraph)


def test_add_class(sample_hierarchy_graph):
    sample_hierarchy_graph.add_class("ClassA")
    assert "ClassA" in sample_hierarchy_graph.graph.nodes


def test_add_inheritance(sample_hierarchy_graph):
    sample_hierarchy_graph.add_class("ClassA")
    sample_hierarchy_graph.add_class("ClassB")
    sample_hierarchy_graph.add_inheritance("ClassB", "ClassA")
    assert ("ClassA", "ClassB") in sample_hierarchy_graph.graph.edges


def test_analyze_hierarchy(sample_hierarchy_graph):
    sample_hierarchy_graph.add_class("ClassA")
    sample_hierarchy_graph.add_class("ClassB")
    sample_hierarchy_graph.add_inheritance("ClassB", "ClassA")
    root_classes = sample_hierarchy_graph.analyze_hierarchy()
    assert "ClassA" in root_classes
    assert "ClassB" not in root_classes


# @patch("hierarchy_graph.nx.draw")
# def test_display_graph(mock_draw, sample_hierarchy_graph):
#     sample_hierarchy_graph.add_class("ClassA")
#     sample_hierarchy_graph.display_graph()
#     mock_draw.assert_called_once()

