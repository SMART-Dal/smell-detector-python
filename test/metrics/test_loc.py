import ast

from metrics.loc import method_loc, class_loc


def test_method_loc_with_function():
    source = """
def example(x):
    if x > 0:
        return True
    return False
"""
    node = ast.parse(source).body[0]
    assert method_loc(node) == 4  # 4 lines in the function


def test_method_loc_with_non_function():
    node = ast.parse("x = 5").body[0]
    assert method_loc(node) == 0


def test_class_loc_with_class():
    source = """
class Example:
    def method1(self):
        pass

    def method2(self):
        if True:
            pass
        return
"""
    node = ast.parse(source).body[0]
    assert class_loc(node) == 8  # 8 lines in the class


def test_class_loc_with_nested_class():
    source = """
class Outer:
    class Inner:
        def method(self):
            pass
"""
    node = ast.parse(source).body[0]
    assert class_loc(node) == 4  # 4 lines in the outer class, including the inner class


def test_class_loc_with_non_class():
    node = ast.parse("def example(): pass").body[0]
    assert class_loc(node) == 0
