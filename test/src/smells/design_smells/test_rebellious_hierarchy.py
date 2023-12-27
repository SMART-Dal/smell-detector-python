import logging
from unittest.mock import create_autospec, MagicMock

import pytest

from src.smells.design_smells import RebelliousHierarchyDetector
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_method import SMMethod
from src.sourcemodel.sm_module import SMModule
from src.sourcemodel.sm_project import SMProject


# Fixtures
@pytest.fixture
def detector():
    return RebelliousHierarchyDetector()


@pytest.fixture
def simple_method():
    method = create_autospec(SMMethod, instance=True)
    method.name = "simple_method"
    method.ast_node = MagicMock()  # Add more details as needed for your AST node
    return method


@pytest.fixture
def simple_class(simple_method):
    sm_class = create_autospec(SMClass, instance=True)
    sm_class.name = "SimpleClass"
    sm_class.start_line = 1
    sm_class.super_classes = []
    sm_class.methods = [simple_method]
    return sm_class


@pytest.fixture
def mock_module(simple_class):
    module = create_autospec(SMModule, instance=True)
    module.name = "TestModule"
    module.classes = [simple_class]
    module.project = create_autospec(SMProject, instance=True)
    return module


@pytest.fixture
def rebellious_class(simple_method):
    sm_class = create_autospec(SMClass, instance=True)
    sm_class.name = "RebelliousClass"
    sm_class.start_line = 1
    sm_class.super_classes = ["SuperClass"]
    sm_class.methods = [simple_method]
    return sm_class


# Mocks for your detector methods
def mocked_is_method_rebellious(method, sm_class, project):
    if method.name == "simple_method" and sm_class.name == "RebelliousClass":
        return True  # Indicate that this method is rebellious
    return False


def mocked_find_method_in_class(method_name, sm_class):
    if method_name == "simple_method" and sm_class.name == "SuperClass":
        super_method = create_autospec(SMMethod, instance=True)
        super_method.name = method_name
        return super_method  # Return a mocked method as if it were found in the superclass
    return None


# Test cases
def test_rebellious_hierarchy_detection(detector, mock_module, rebellious_class, caplog, mocker):
    mocker.patch('src.smells.design_smells.RebelliousHierarchyDetector.is_method_rebellious',
                 side_effect=mocked_is_method_rebellious)
    mocker.patch('src.smells.design_smells.RebelliousHierarchyDetector.find_method_in_class',
                 side_effect=mocked_find_method_in_class)
    mock_module.classes = [rebellious_class]
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 1, "Should detect one rebellious hierarchy smell."


def test_no_rebellious_hierarchy(detector, mock_module):
    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 0, "Should not detect any rebellious hierarchy smells for a simple class."


def test_rebellious_hierarchy_with_config(detector, mock_module, rebellious_class, mocker):
    mocker.patch('src.smells.design_smells.RebelliousHierarchyDetector.is_method_rebellious', return_value=True)
    mocker.patch('src.smells.design_smells.RebelliousHierarchyDetector.find_method_in_class', return_value=None)

    mock_module.classes = [rebellious_class]

    # Provide a custom configuration
    custom_config = {'some_config': 'custom_value'}
    smells = detector._detect_smells(mock_module, custom_config)
    assert len(smells) == 1, "Should still detect a rebellious hierarchy smell with custom configuration."


def test_rebellious_in_complex_hierarchy(detector, mock_module, mocker, rebellious_class):
    base_class = create_autospec(SMClass, instance=True, start_line=1)
    base_class.name = "BaseClass"
    intermediate_class = create_autospec(SMClass, instance=True, start_line=1,
                                         super_classes=["BaseClass"])
    intermediate_class.name = "IntermediateClass"
    rebellious_class = create_autospec(SMClass, instance=True, start_line=1,
                                       super_classes=["IntermediateClass"])
    rebellious_class.name = "RebelliousClass"
    method = create_autospec(SMMethod, instance=True, name="complex_method")
    rebellious_class.methods = [method]

    mock_module.classes = [rebellious_class, intermediate_class, base_class]

    mocker.patch('src.smells.design_smells.RebelliousHierarchyDetector.is_method_rebellious', return_value=True)
    mocker.patch('src.smells.design_smells.RebelliousHierarchyDetector.find_method_in_class', return_value=method)

    smells = detector._detect_smells(mock_module, {})
    assert len(smells) == 1, "Should detect a rebellious hierarchy smell in a complex class hierarchy."


def test_error_logging_on_failed_analysis(detector, mock_module, rebellious_class, caplog):
    def raise_exception():
        raise Exception("Method analysis failed")

    rebellious_class.methods = raise_exception
    mock_module.classes = [rebellious_class]
    with caplog.at_level(logging.ERROR):
        detector._detect_smells(mock_module, {})
        assert "Error checking Rebellious Hierarchy" in caplog.text, "Should log an error if method analysis fails."
