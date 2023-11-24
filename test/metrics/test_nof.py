import ast

from metrics.nof import number_of_fields, number_of_public_fields


def test_number_of_fields_with_class():
    source = """
class Example:
    field1 = 1
    field2 = 2
    _private_field = 3
"""
    node = ast.parse(source).body[0]
    assert number_of_fields(node) == 3  # 3 fields in total


def test_number_of_public_fields_with_class():
    source = """
class Example:
    field1 = 1
    field2 = 2
    _private_field = 3
"""
    node = ast.parse(source).body[0]
    assert number_of_public_fields(node) == 2  # 2 public fields


def test_number_of_fields_with_no_fields_class():
    source = """
class Example:
    def method(self):
        pass
"""
    node = ast.parse(source).body[0]
    assert number_of_fields(node) == 0  # No fields


def test_number_of_public_fields_with_non_class():
    node = ast.parse("def example(): pass").body[0]
    assert number_of_public_fields(node) == 0


def test_number_of_fields_with_non_class():
    node = ast.parse("x = 5").body[0]
    assert number_of_fields(node) == 0
