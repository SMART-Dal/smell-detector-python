import pytest

from sourcemodel.sm_method import PyMethod


def test_method_initialization():
    method = PyMethod("testMethod", 1, 5, "public", ["@decorator"])
    assert method.name == "testMethod"
    assert method.start_line == 1
    assert method.end_line == 5
    assert method.access_modifier == "public"
    assert method.decorators == ["@decorator"]


def test_method_with_empty_decorators():
    method = PyMethod("testMethod", 1, 5, "public", [])
    assert method.decorators == []


def test_method_with_multiple_decorators():
    method = PyMethod("testMethod", 1, 5, "public", ["@decorator1", "@decorator2"])
    assert method.decorators == ["@decorator1", "@decorator2"]
