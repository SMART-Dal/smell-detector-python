import pytest
from unittest.mock import Mock

from sourcemodel.sm_package import PyPackage


@pytest.fixture
def sample_pypackage():
    return PyPackage("TestPackage")


def test_pypackage_initialization(sample_pypackage):
    assert sample_pypackage.name == "TestPackage"
    assert sample_pypackage.modules == []


def test_add_module(sample_pypackage):
    mock_module = Mock()
    sample_pypackage.add_module(mock_module)
    assert mock_module in sample_pypackage.modules


def test_analyze(sample_pypackage):
    mock_module = Mock()
    sample_pypackage.add_module(mock_module)
    sample_pypackage.analyze()
    mock_module.analyze.assert_called_once()

