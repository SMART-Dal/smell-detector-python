import pytest
import networkx as nx
from unittest.mock import Mock, patch

from sourcemodel.dependency_graph import DependencyGraph


@pytest.fixture
def sample_dependency_graph():
    return DependencyGraph()


def test_initialization(sample_dependency_graph):
    assert isinstance(sample_dependency_graph.graph, nx.DiGraph)


def test_add_module(sample_dependency_graph):
    sample_dependency_graph.add_module("module1")
    assert "module1" in sample_dependency_graph.graph.nodes


def test_add_dependency(sample_dependency_graph):
    sample_dependency_graph.add_module("module1")
    sample_dependency_graph.add_module("module2")
    sample_dependency_graph.add_dependency("module1", "module2")
    assert ("module1", "module2") in sample_dependency_graph.graph.edges


def test_analyze_dependencies(sample_dependency_graph):
    sample_dependency_graph.add_module("module1")
    sample_dependency_graph.add_module("module2")
    sample_dependency_graph.add_dependency("module1", "module2")
    most_dependent_modules = sample_dependency_graph.analyze_dependencies()
    assert most_dependent_modules[0][0] == "module1"


# @patch("dependency_graph.nx.draw")
# def test_display_graph(mock_draw, sample_dependency_graph):
#     sample_dependency_graph.add_module("module1")
#     sample_dependency_graph.display_graph()
#     mock_draw.assert_called_once()

