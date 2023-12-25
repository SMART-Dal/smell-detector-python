import logging

import pytest
from unittest.mock import MagicMock

from src.smells.implementation_smells import LongMethodDetector

# Sample data for testing
short_method = MagicMock()
short_method.loc = 10
short_method.name = "short_method"
short_method.start_line = 1
short_method.end_line = 10

long_method = MagicMock()
long_method.loc = 25
long_method.name = "long_method"
long_method.start_line = 20
long_method.end_line = 45


@pytest.fixture
def mock_module():
    module = MagicMock()
    module.name = "test_module"
    module.functions = [short_method, long_method]
    module.classes = []  # Assuming no methods for simplicity
    return module


@pytest.fixture
def detector():
    return LongMethodDetector()


# Test for methods with an acceptable length
def test_no_long_methods(detector, mock_module):
    smells = detector.detect(mock_module, {"threshold": 20})
    assert not any(
        smell['entity_name'] == short_method.name for smell in smells), "Should not detect smells in short methods"


# Test for long methods
def test_long_methods(detector, mock_module):
    smells = detector.detect(mock_module, {"threshold": 20})
    assert any(smell['entity_name'] == long_method.name for smell in smells), "Should detect smells in long methods"


# Test error handling
def test_error_handling(detector, mock_module, caplog):
    mock_module.functions = [MagicMock(side_effect=Exception("Test Exception"))]
    with caplog.at_level(logging.ERROR):
        smells = detector.detect(mock_module, {"threshold": 20})
    assert "Error analyzing" in caplog.text, "Should log analysis errors"
    assert len(smells) == 0, "Should not return any smells when an error occurs"


# Test configuration respect
def test_configuration_respect(detector, mock_module):
    smells = detector.detect(mock_module, {"threshold": 30})
    assert not any(smell['entity_name'] == long_method.name for smell in
                   smells), "Should not detect smells when the threshold is high enough"
