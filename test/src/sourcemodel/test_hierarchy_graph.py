import networkx as nx
import pytest

from src.sourcemodel.hierarchy_graph import HierarchyGraph


@pytest.fixture
def hierarchy_graph_instance():
    return HierarchyGraph()


# Test adding a class to the graph
def test_add_class(hierarchy_graph_instance):
    hierarchy_graph_instance.add_class("BaseClass")
    assert "BaseClass" in hierarchy_graph_instance.graph.nodes, "Class should be added to the graph"


# Test adding inheritance relationship between classes
def test_add_inheritance(hierarchy_graph_instance):
    hierarchy_graph_instance.add_class("BaseClass")
    hierarchy_graph_instance.add_class("DerivedClass")
    hierarchy_graph_instance.add_inheritance("DerivedClass", "BaseClass")

    assert "BaseClass" in hierarchy_graph_instance.graph.nodes, "Parent class should be in the graph"
    assert "DerivedClass" in hierarchy_graph_instance.graph.nodes, "Child class should be in the graph"
    assert ("BaseClass",
            "DerivedClass") in hierarchy_graph_instance.graph.edges, "Inheritance relationship should be added"


# Test adding duplicate classes
def test_add_duplicate_class(hierarchy_graph_instance):
    hierarchy_graph_instance.add_class("BaseClass")
    hierarchy_graph_instance.add_class("BaseClass")
    assert len(hierarchy_graph_instance.graph.nodes) == 1, "Duplicate class should not be added"


# Test adding cyclic inheritance (which should not be allowed)
def test_add_cyclic_inheritance(hierarchy_graph_instance):
    hierarchy_graph_instance.add_class("ClassA")
    hierarchy_graph_instance.add_class("ClassB")
    hierarchy_graph_instance.add_class("ClassC")

    # Creating a cyclic inheritance relationship
    hierarchy_graph_instance.add_inheritance("ClassA", "ClassB")
    hierarchy_graph_instance.add_inheritance("ClassB", "ClassC")
    hierarchy_graph_instance.add_inheritance("ClassC", "ClassA")

    assert not nx.is_directed_acyclic_graph(hierarchy_graph_instance.graph), "Cyclic inheritance should not be allowed"

