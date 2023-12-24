# Fixture for creating a DependencyGraph instance
import networkx as nx
import pytest

from src.sourcemodel.dependency_graph import DependencyGraph


@pytest.fixture
def dependency_graph_instance():
    return DependencyGraph()


# Test adding a module to the graph
def test_add_module(dependency_graph_instance):
    dependency_graph_instance.add_module("module1")
    assert "module1" in dependency_graph_instance.graph.nodes, "Module should be added to the graph"


# Test adding a dependency between modules
def test_add_dependency(dependency_graph_instance):
    dependency_graph_instance.add_module("module1")
    dependency_graph_instance.add_module("module2")
    dependency_graph_instance.add_dependency("module1", "module2.py")

    assert "module1" in dependency_graph_instance.graph.nodes, "Source module should be in the graph"
    assert "module2.py" in dependency_graph_instance.graph.nodes, "Target module should be in the graph"
    assert ("module1", "module2.py") in dependency_graph_instance.graph.edges, "Dependency should be added"


# Test adding duplicate modules
def test_add_duplicate_module(dependency_graph_instance):
    dependency_graph_instance.add_module("module1")
    dependency_graph_instance.add_module("module1")
    assert len(dependency_graph_instance.graph.nodes) == 1, "Duplicate module should not be added"


# Test adding dependencies between modules
def test_add_multiple_dependencies(dependency_graph_instance):
    dependency_graph_instance.add_module("module1")
    dependency_graph_instance.add_module("module2")
    dependency_graph_instance.add_dependency("module1", "module2.py")
    dependency_graph_instance.add_dependency("module1", "module3.py")

    assert len(dependency_graph_instance.graph.edges) == 2, "Multiple dependencies should be added"


