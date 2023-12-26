import logging

import pytest
from unittest.mock import create_autospec, MagicMock, PropertyMock
from src.smells.design_smells import MultipathHierarchyDetector
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_module import SMModule
from src.sourcemodel.hierarchy_graph import HierarchyGraph
from src.sourcemodel.sm_project import SMProject


# Fixtures for setting up the necessary objects
@pytest.fixture
def detector():
    return MultipathHierarchyDetector()


@pytest.fixture
def sm_class():
    return create_autospec(SMClass, instance=True, name="SampleClass", start_line=1)


@pytest.fixture
def hierarchy_graph(mocker):
    hg = create_autospec(HierarchyGraph)
    mocker.patch.object(hg, 'has_multipath_inheritance', return_value=(True, "CommonAncestor"))
    return hg


@pytest.fixture
def mock_module(sm_class, hierarchy_graph):
    module = create_autospec(SMModule, instance=True)
    module.name = "TestModule"
    module.project = create_autospec(SMProject, instance=True)
    module.classes = [sm_class]
    module.project.hierarchy_graph = hierarchy_graph
    return module


def test_multipath_hierarchy_detection(detector, mock_module, sm_class):
    sm_class.name = "ClassWithMultipath"
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 1, "Should detect one multipath hierarchy smell."
    detected_smell_detail = smells[0]['details']
    assert "ClassWithMultipath" in detected_smell_detail and "CommonAncestor" in detected_smell_detail, \
        "The smell detail should correctly describe the multipath inheritance issue."


def test_no_multipath_hierarchy_detected(detector, mock_module, sm_class, hierarchy_graph):
    hierarchy_graph.has_multipath_inheritance.return_value = (False, None)
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Should not detect multipath hierarchy smell when it's not present."


def test_error_handling_in_class_level(detector, mock_module, caplog):
    def raise_exception(*args, **kwargs):
        raise Exception("Depth Calculation Error")

    mock_module.project.hierarchy_graph.get_inheritance_depth.side_effect = raise_exception
    with caplog.at_level(logging.ERROR):
        detector._detect_smells(mock_module, {'max_depth': 4})
        assert "Error detecting Multipath Hierarchy" in caplog.text, \
            "Should log an error for exceptions during depth calculation for a class."


def test_error_handling_in_module_level(detector, mock_module, caplog):
    faulty_module = MagicMock(spec=SMModule)

    def raise_exception(*args, **kwargs):
        raise Exception("Module Exception")
    faulty_module.classes = raise_exception
    faulty_module.name = "FaultyModule"  # Ensure the name attribute is set for logging
    with caplog.at_level(logging.ERROR):
        detector._detect_smells(faulty_module, {'max_depth': 4})
        assert "Error detecting Multipath Hierarchy" in caplog.text, \
            "Should log an error for exceptions during smell detection at the module level."
