import ast

from metrics.nom import number_of_methods, number_of_public_methods


def test_number_of_methods_with_class():
    source = """
class Example:
    def method1(self):
        pass
    def method2(self):
        pass
    def _private_method(self):
        pass
"""
    node = ast.parse(source).body[0]
    assert number_of_methods(node) == 3  # 3 methods in total


def test_number_of_public_methods_with_class():
    source = """
class Example:
    def method1(self):
        pass
    def method2(self):
        pass
    def _private_method(self):
        pass
"""
    node = ast.parse(source).body[0]
    assert number_of_public_methods(node) == 2  # 2 public methods


def test_number_of_methods_with_no_methods_class():
    source = """
class Example:
    field = 1
"""
    node = ast.parse(source).body[0]
    assert number_of_methods(node) == 0  # No methods


def test_number_of_public_methods_with_non_class():
    node = ast.parse("def example(): pass").body[0]
    assert number_of_public_methods(node) == 0


def test_number_of_methods_with_non_class():
    node = ast.parse("x = 5").body[0]
    assert number_of_methods(node) == 0
