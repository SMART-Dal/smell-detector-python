import ast

from metrics.wmc import weighted_methods_per_class


def test_weighted_methods_per_class_with_class():
    source = """
class Example:
    def method1(self):
        if True: pass

    def method2(self):
        for i in range(3): pass
"""
    node = ast.parse(source).body[0]
    assert weighted_methods_per_class(node) == 3  # method1: complexity 2, method2: complexity 1


def test_weighted_methods_per_class_with_no_methods():
    source = """
class Example:
    field = 1
"""
    node = ast.parse(source).body[0]
    assert weighted_methods_per_class(node) == 0  # No methods


def test_weighted_methods_per_class_with_non_class():
    node = ast.parse("def example(): pass").body[0]
    assert weighted_methods_per_class(node) == 0


def test_weighted_methods_with_complex_methods():
    source = """
class Example:
    def method1(self):
        if x > 0 and y < 0:
            pass
        elif x > 10:
            for i in range(10):
                pass
"""
    node = ast.parse(source).body[0]
    assert weighted_methods_per_class(node) == 4  # Complex method with multiple branches


def test_weighted_methods_empty_class():
    source = "class Example: pass"
    node = ast.parse(source).body[0]
    assert weighted_methods_per_class(node) == 0  # Empty class


def test_weighted_methods_class_with_non_method_members():
    source = """
class Example:
    field = 10
    def method(self): pass
"""
    node = ast.parse(source).body[0]
    assert weighted_methods_per_class(node) == 1  # Only one simple method


def test_weighted_methods_class_with_only_docstrings():
    source = '''
class Example:
    def method(self):
        """This is a docstring"""
'''
    node = ast.parse(source).body[0]
    assert weighted_methods_per_class(node) == 1  # Method with only a docstring
