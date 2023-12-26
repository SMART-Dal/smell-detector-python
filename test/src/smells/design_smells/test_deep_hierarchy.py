import logging
from unittest.mock import create_autospec, MagicMock

import pytest

from src.smells.design_smells import DeepHierarchyDetector
from src.sourcemodel.hierarchy_graph import HierarchyGraph
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_module import SMModule


@pytest.fixture
def detector():
    return DeepHierarchyDetector()


@pytest.fixture
def shallow_class():
    sm_class = create_autospec(SMClass)
    sm_class.name = "ShallowClass"
    sm_class.start_line = 1
    return sm_class


@pytest.fixture
def deep_class():
    sm_class = create_autospec(SMClass)
    sm_class.name = "DeepClass"
    sm_class.start_line = 1
    return sm_class


@pytest.fixture
def hierarchy_graph():
    graph = create_autospec(HierarchyGraph)
    graph.get_inheritance_depth.side_effect = lambda name: 2 if name == "ShallowClass" else 5
    return graph


@pytest.fixture
def mock_project(hierarchy_graph):
    project = MagicMock()
    project.hierarchy_graph = hierarchy_graph
    return project


@pytest.fixture
def mock_module(mock_project, shallow_class, deep_class):
    module = create_autospec(SMModule)
    module.name = "TestModule"
    module.classes = [shallow_class, deep_class]
    module.project = mock_project
    return module


def test_no_deep_hierarchy(detector, mock_module, shallow_class):
    smells = detector._detect_smells(mock_module, {'max_depth': 4})
    assert not any(smell['entity_name'] == shallow_class.name for smell in smells), \
        "No deep hierarchy smell should be detected for a shallow class."


def test_detect_deep_hierarchy(detector, mock_module, deep_class):
    smells = detector._detect_smells(mock_module, {'max_depth': 4})
    assert any(smell['entity_name'] == deep_class.name for smell in smells), \
        "Deep hierarchy smell should be detected for a deep class."


def test_customizable_depth_threshold(detector, mock_module, deep_class):
    custom_max_depth = 3
    smells = detector._detect_smells(mock_module, {'max_depth': custom_max_depth})
    assert all(smell['details'].endswith(f"a depth of 5.") for smell in smells), \
        "The reported depth should match the actual depth in the hierarchy."


def test_detect_deep_hierarchy_with_logging(detector, mock_module, deep_class, caplog):
    with caplog.at_level(logging.ERROR):
        smells = detector._detect_smells(mock_module, {'max_depth': 4})
        assert any(smell['entity_name'] == deep_class.name for smell in smells), \
            "Deep hierarchy smell should be detected for a deep class."
        assert "Error calculating depth" not in caplog.text, \
            "No error should be logged when successfully calculating depth."


def test_error_handling_depth_calculation(detector, mock_module, deep_class, caplog):
    def raise_exception(*args, **kwargs):
        raise Exception("Depth Calculation Error")

    mock_module.project.hierarchy_graph.get_inheritance_depth.side_effect = raise_exception
    with caplog.at_level(logging.ERROR):
        detector._detect_smells(mock_module, {'max_depth': 4})
        assert "Error calculating depth for class" in caplog.text, \
            "Should log an error for exceptions during depth calculation."


def test_error_handling_module_iteration(detector, caplog):
    faulty_module = MagicMock(spec=SMModule)

    def raise_exception(*args, **kwargs):
        raise Exception("Module Iteration Error")

    faulty_module.classes = raise_exception
    faulty_module.name = "FaultyModule"  # Ensure the name attribute is set for logging

    with caplog.at_level(logging.ERROR):
        detector._detect_smells(faulty_module, {'max_depth': 4})
        assert "Error detecting Deep Hierarchy smells in module" in caplog.text, \
            "Should log an error for exceptions during module iteration."
