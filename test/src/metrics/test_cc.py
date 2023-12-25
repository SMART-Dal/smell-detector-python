import ast
import logging

import pytest

from src.metrics import calculate_cyclomatic_complexity

# Example code snippets to test
simple_code = "x = 1"
complex_code = """
if x == 1 or y == 2 and z == 3:
    print('Complex logic')
"""


# Fixtures to parse the code into AST nodes
@pytest.fixture
def simple_node():
    return ast.parse(simple_code).body[0]


@pytest.fixture
def complex_node():
    return ast.parse(complex_code).body[0]


# Tests
def test_calculate_cyclomatic_complexity_simple(simple_node):
    complexity = calculate_cyclomatic_complexity(simple_node)
    assert complexity == 1, "Cyclomatic complexity of simple code should be 1"


def test_calculate_cyclomatic_complexity_complex(complex_node):
    complexity = calculate_cyclomatic_complexity(complex_node)
    assert complexity > 1, "Cyclomatic complexity of complex code should be greater than 1"


def test_calculate_cyclomatic_complexity_invalid_input(caplog):
    with caplog.at_level(logging.ERROR):
        complexity = calculate_cyclomatic_complexity(None)
    assert complexity == 0, "Should return 0 for invalid input"
    assert "Invalid input" in caplog.text, "Should log an error for invalid input"
