import logging
from unittest.mock import create_autospec, MagicMock

import pytest

from src.smells.design_smells import WideHierarchyDetector
from src.sourcemodel.hierarchy_graph import HierarchyGraph
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_module import SMModule


@pytest.fixture
def detector():
    return WideHierarchyDetector()


@pytest.fixture
def py_class():
    return create_autospec(SMClass, instance=True, name="ParentClass", start_line=1)


@pytest.fixture
def hierarchy_graph(mocker):
    hg = MagicMock(spec=HierarchyGraph)
    hg.graph = MagicMock()
    hg.graph.successors.return_value = ["ChildClass1", "ChildClass2", "ChildClass3", "ChildClass4", "ChildClass5",
                                        "ChildClass6"]
    return hg


@pytest.fixture
def mock_module(py_class, hierarchy_graph):
    module = create_autospec(SMModule, instance=True)
    module.name = "TestModule"
    module.classes = [py_class]
    module.project = MagicMock()
    module.project.hierarchy_graph = hierarchy_graph
    return module


def test_wide_hierarchy_detection(detector, mock_module, py_class):
    py_class.name = "ParentClass"

    smells = detector._detect_smells(mock_module, {'threshold': 5})
    assert len(smells) == 1, "Should detect a wide hierarchy smell."
    assert "ParentClass" in smells[0]['details'], "The smell detail should correctly identify the parent class."


def test_no_wide_hierarchy(detector, mock_module, py_class, hierarchy_graph):
    hierarchy_graph.graph.successors.return_value = ["ChildClass1", "ChildClass2"]
    smells = detector._detect_smells(mock_module, {'threshold': 5})
    assert len(
        smells) == 0, "Should not detect a wide hierarchy smell when the number of children is below the threshold."


def test_wide_hierarchy_with_custom_threshold(detector, mock_module, py_class, hierarchy_graph):
    py_class.name = "ParentClass"
    custom_threshold = 3
    hierarchy_graph.graph.successors.return_value = ["ChildClass1", "ChildClass2", "ChildClass3", "ChildClass4"]
    smells = detector._detect_smells(mock_module, {'threshold': custom_threshold})
    assert len(smells) == 1, f"Should detect a wide hierarchy smell with a custom threshold of {custom_threshold}."
    assert "ParentClass" in smells[0]['details'], "The smell detail should correctly identify the parent class."


def test_no_classes_in_module(detector, mock_module, hierarchy_graph):
    mock_module.classes = []
    smells = detector._detect_smells(mock_module, {'threshold': 5})
    assert len(smells) == 0, "Should not detect any smells when there are no classes in the module."


def test_nonexistent_superclasses(detector, mock_module, py_class, hierarchy_graph):
    mock_module.project.find_class.return_value = None
    smells = detector._detect_smells(mock_module, {'threshold': 5})
    assert len(smells) == 0, "Should handle nonexistent superclasses gracefully without detecting false positives."


def test_multiple_wide_hierarchies(detector, mock_module, hierarchy_graph):
    class1 = create_autospec(SMClass, instance=True, name="ParentClass1", start_line=1)
    class1.name = "ParentClass1"
    class2 = create_autospec(SMClass, instance=True, name="ParentClass2", start_line=2)
    class2.name = "ParentClass2"
    mock_module.classes = [class1, class2]
    hierarchy_graph.graph.successors.return_value = ["ChildClass1", "ChildClass2", "ChildClass3", "ChildClass4",
                                                     "ChildClass5", "ChildClass6"]
    smells = detector._detect_smells(mock_module, {'threshold': 5})
    assert len(smells) == 2, "Should detect wide hierarchy smells for multiple classes."


def test_single_child(detector, mock_module, py_class, hierarchy_graph):
    hierarchy_graph.graph.successors.return_value = ["ChildClass1"]
    smells = detector._detect_smells(mock_module, {'threshold': 5})
    assert len(smells) == 0, "Should not detect a wide hierarchy smell for a single child."


def test_error_handling(detector, mock_module, caplog):
    mock_module.project.hierarchy_graph.graph.successors.side_effect = Exception("Test occurred")
    with caplog.at_level(logging.ERROR):
        detector._detect_smells(mock_module, {'threshold': 5})
        assert "Error detecting Wide Hierarchy smells" in caplog.text, "Should log an error message when an exception occurs."

