import ast

from metrics.cc import cyclomatic_complexity


def test_cyclomatic_complexity_with_function():
    source = """
def example(x):
    if x > 0:
        return True
    else:
        return False
"""
    node = ast.parse(source).body[0]
    assert cyclomatic_complexity(node) == 2  # 1 for the function itself, 1 for the if statement


def test_cyclomatic_complexity_with_non_function():
    node = ast.parse("x = 5").body[0]
    assert cyclomatic_complexity(node) == 0


def test_cyclomatic_complexity_with_no_control_structure():
    source = """
def example(x):
    return x * 2
"""
    node = ast.parse(source).body[0]
    assert cyclomatic_complexity(node) == 1  # Just the function itself, no control structures


def test_cyclomatic_complexity_with_multiple_controls():
    source = """
def example(x):
    if x > 0:
        while x < 10:
            x += 1
    return x
"""
    node = ast.parse(source).body[0]
    assert cyclomatic_complexity(node) == 3  # Function, if, and while


def test_cyclomatic_complexity_with_logical_operators():
    source = """
def example(x, y):
    if x > 0 and y < 0:
        return True
    return False
"""
    node = ast.parse(source).body[0]
    assert cyclomatic_complexity(node) == 3  # Function and two conditions in the if statement
