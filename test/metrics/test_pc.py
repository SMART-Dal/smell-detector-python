import ast

from metrics.pc import parameter_count


def test_parameter_count_with_function_no_params():
    source = "def example(): pass"
    node = ast.parse(source).body[0]
    assert parameter_count(node) == 0  # No parameters


def test_parameter_count_with_function_single_param():
    source = "def example(param1): pass"
    node = ast.parse(source).body[0]
    assert parameter_count(node) == 1  # One parameter


def test_parameter_count_with_function_multiple_params():
    source = "def example(param1, param2, param3): pass"
    node = ast.parse(source).body[0]
    assert parameter_count(node) == 3  # Three parameters


def test_parameter_count_with_non_function():
    node = ast.parse("x = 5").body[0]
    assert parameter_count(node) == 0
