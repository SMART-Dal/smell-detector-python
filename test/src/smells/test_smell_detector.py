import logging
from unittest.mock import MagicMock

import pytest

from src.smells.smell_detector import ImplementationSmellDetector, DesignSmellDetector


# Sample mock class and function objects for testing purposes
@pytest.fixture
def mock_module():
    module = MagicMock()
    module.name = "SampleModule"
    module.functions = [MagicMock(name="Function1"), MagicMock(name="Function2")]
    module.classes = [MagicMock(name="Class1", methods=[MagicMock(name="Method1"), MagicMock(name="Method2")])]
    return module


@pytest.fixture
def mock_config():
    return {'detect': True}


# Concrete implementations for testing
class MockImplementationDetector(ImplementationSmellDetector):
    def _detect_smells(self, module, config):
        return [{'smell': 'ImplementationSmell'}] if config.get('detect') else []


class MockDesignDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        return [{'smell': 'DesignSmell'}] if config.get('detect') else []


@pytest.fixture
def implementation_detector():
    return MockImplementationDetector()


@pytest.fixture
def design_detector():
    return MockDesignDetector()


# Tests for ImplementationSmellDetector
def test_implementation_smell_detection_success(implementation_detector, mock_module, mock_config):
    smells = implementation_detector.detect(mock_module, mock_config)
    assert len(smells) > 0, "Should detect smells when enabled"


def test_implementation_smell_detection_disabled(implementation_detector, mock_module):
    smells = implementation_detector.detect(mock_module, {'detect': False})
    assert len(smells) == 0, "Should not detect smells when disabled"


def test_implementation_smell_detection_error_handling(implementation_detector, mock_module, caplog, mocker):
    mocker.patch.object(implementation_detector, '_detect_smells', side_effect=Exception("Unexpected Error"))
    with caplog.at_level(logging.ERROR):
        implementation_detector.detect(mock_module, {'detect': True})
    assert "Error detecting implementation smells" in caplog.text, "Error should be logged"


def test_design_smell_detection_success(design_detector, mock_module, mock_config):
    smells = design_detector.detect(mock_module, mock_config)
    assert len(smells) > 0, "Should detect smells when enabled"


def test_design_smell_detection_disabled(design_detector, mock_module):
    smells = design_detector.detect(mock_module, {'detect': False})
    assert len(smells) == 0, "Should not detect smells when disabled"


def test_design_smell_detection_error_handling(design_detector, mock_module, caplog, mocker):
    mocker.patch.object(design_detector, '_detect_smells', side_effect=Exception("Unexpected Error"))
    with caplog.at_level(logging.ERROR):
        smells = design_detector.detect(mock_module, {'detect': True})
    assert "Error detecting design smells" in caplog.text
    assert len(smells) == 0, "Should return an empty list on error"
