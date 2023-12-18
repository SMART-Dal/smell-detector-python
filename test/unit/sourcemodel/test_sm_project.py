import pytest

from src.sourcemodel.sm_project import PyProject


# Fixtures to provide mocked modules and packages
@pytest.fixture
def mock_module(mocker):
    return mocker.MagicMock(name='MockModule')


@pytest.fixture
def mock_class(mocker):
    mock_class = mocker.MagicMock(name='MockClass')
    mock_class.name = "TestClass"
    return mock_class


@pytest.fixture
def mock_package(mocker):
    return mocker.MagicMock(name='MockPackage')


@pytest.fixture
def py_project():
    return PyProject(name='TestProject')


# Tests start here
def test_add_module(py_project, mock_module):
    py_project.add_module(mock_module)
    assert mock_module in py_project.modules, "Module should be added to the project's modules list"
    assert mock_module.dependency_graph == py_project.dependency_graph, "Module's dependency graph should be set"


def test_add_package(py_project, mock_package):
    py_project.add_package(mock_package)
    assert mock_package in py_project.packages, "Package should be added to the project's packages list"


def test_analyze_project(py_project, mock_module):
    py_project.add_module(mock_module)
    py_project.analyze_project()
    mock_module.analyze.assert_called_once_with(), "Module's analyze method should be called"


def test_find_class_found(py_project, mock_module, mock_class):
    class_name = "TestClass"
    mock_module.classes = [mock_class]
    py_project.add_module(mock_module)

    found_class = py_project.find_class(class_name)
    assert found_class is not None, "Should find the class when it exists"
    assert found_class.name == class_name, "Found class should have the correct name"



def test_find_class_not_found(py_project, mock_module):
    class_name = "NonExistentClass"
    py_project.add_module(mock_module)
    found_class = py_project.find_class(class_name)
    assert found_class is None, "Should return None when the class does not exist"

