import pytest
from unittest.mock import Mock

from sourcemodel.sm_class import PyClass


@pytest.fixture
def sample_pyclass():
    return PyClass("TestClass", 1, 10)


def test_pyclass_initialization(sample_pyclass):
    assert sample_pyclass.name == "TestClass"
    assert sample_pyclass.start_line == 1
    assert sample_pyclass.end_line == 10
    assert isinstance(sample_pyclass.methods, list)
    assert isinstance(sample_pyclass.class_variables, list)
    assert isinstance(sample_pyclass.base_classes, list)
    assert isinstance(sample_pyclass.nested_classes, list)


def test_add_method(sample_pyclass):
    mock_method = Mock()
    sample_pyclass.add_method(mock_method)
    assert mock_method in sample_pyclass.methods


def test_add_variable(sample_pyclass):
    mock_variable = Mock()
    sample_pyclass.add_variable(mock_variable)
    assert mock_variable in sample_pyclass.class_variables


def test_add_nested_class(sample_pyclass):
    mock_nested_class = Mock()
    sample_pyclass.add_nested_class(mock_nested_class)
    assert mock_nested_class in sample_pyclass.nested_classes


def test_method_list_integrity(sample_pyclass):
    mock_method1 = Mock()
    mock_method2 = Mock()
    sample_pyclass.add_method(mock_method1)
    sample_pyclass.add_method(mock_method2)
    assert sample_pyclass.methods == [mock_method1, mock_method2]


def test_variable_list_integrity(sample_pyclass):
    mock_variable1 = Mock()
    mock_variable2 = Mock()
    sample_pyclass.add_variable(mock_variable1)
    sample_pyclass.add_variable(mock_variable2)
    assert sample_pyclass.class_variables == [mock_variable1, mock_variable2]


def test_nested_class_list_integrity(sample_pyclass):
    mock_nested_class1 = Mock()
    mock_nested_class2 = Mock()
    sample_pyclass.add_nested_class(mock_nested_class1)
    sample_pyclass.add_nested_class(mock_nested_class2)
    assert sample_pyclass.nested_classes == [mock_nested_class1, mock_nested_class2]
