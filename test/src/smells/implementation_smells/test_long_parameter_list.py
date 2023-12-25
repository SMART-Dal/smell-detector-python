import logging

import pytest
from unittest.mock import MagicMock

from src.smells.implementation_smells import LongParameterListDetector

# Sample data for testing
function_with_many_params = MagicMock()
function_with_many_params.parameter_count = 10
function_with_many_params.name = "function_with_many_params"
function_with_many_params.start_line = 1
function_with_many_params.end_line = 10

function_with_few_params = MagicMock()
function_with_few_params.parameter_count = 2
function_with_few_params.name = "function_with_few_params"
function_with_few_params.start_line = 20
function_with_few_params.end_line = 30


@pytest.fixture
def mock_module():
    module = MagicMock()
    module.name = "test_module"
    module.functions = [function_with_many_params, function_with_few_params]
    module.classes = []  # Assuming no methods for simplicity
    return module


@pytest.fixture
def detector():
    return LongParameterListDetector()


# Test for functions with an acceptable number of parameters
def test_no_long_parameter_lists(detector, mock_module):
    smells = detector.detect(mock_module, {"threshold": 5})
    assert not any(smell['entity_name'] == function_with_few_params.name for smell in
                   smells), "Should not detect smells in functions with few parameters"


# Test for functions with too many parameters
def test_long_parameter_lists(detector, mock_module):
    smells = detector.detect(mock_module, {"threshold": 5})
    assert any(smell['entity_name'] == function_with_many_params.name for smell in
               smells), "Should detect smells in functions with many parameters"


# Test error handling
def test_error_handling(detector, mock_module, caplog):
    mock_module.functions = [MagicMock(side_effect=Exception("Test Exception"))]
    with caplog.at_level(logging.ERROR):
        smells = detector.detect(mock_module, {"threshold": 5})
    assert "Error analyzing" in caplog.text, "Should log analysis errors"
    assert len(smells) == 0, "Should not return any smells when an error occurs"


# Test configuration respect
def test_configuration_respect(detector, mock_module):
    smells = detector.detect(mock_module, {"threshold": 15})
    assert not any(smell['entity_name'] == function_with_many_params.name for smell in
                   smells), "Should not detect smells when the threshold is high enough"
