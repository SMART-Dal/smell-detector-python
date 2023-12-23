import pytest
from unittest.mock import Mock

from sourcemodel.sm_project import PyProject


@pytest.fixture
def sample_project():
    return PyProject("TestProject")


def test_project_initialization(sample_project):
    assert sample_project.name == "TestProject"
    assert sample_project.modules == []
    assert sample_project.packages == []
    assert sample_project.hierarchy_graph is not None
    assert sample_project.dependency_graph is not None


def test_add_module(sample_project):
    mock_module = Mock()
    sample_project.add_module(mock_module)
    assert mock_module in sample_project.modules


def test_add_package(sample_project):
    mock_package = Mock()
    sample_project.add_package(mock_package)
    assert mock_package in sample_project.packages


def test_analyze_project(sample_project):
    mock_module = Mock()
    sample_project.add_module(mock_module)
    sample_project.analyze_project()
    mock_module.analyze.assert_called_once()
