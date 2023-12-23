import pytest

from sourcemodel.sm_parameter import PyParameter


def test_parameter_initialization():
    param = PyParameter("param1", "int", 10)
    assert param.name == "param1"
    assert param.param_type == "int"
    assert param.default_value == 10


def test_parameter_without_type_and_default():
    param = PyParameter("param2")
    assert param.name == "param2"
    assert param.param_type is None
    assert param.default_value is None


def test_parameter_with_type_only():
    param = PyParameter("param3", "str")
    assert param.name == "param3"
    assert param.param_type == "str"
    assert param.default_value is None


def test_parameter_with_default_only():
    param = PyParameter("param4", default_value=False)
    assert param.name == "param4"
    assert param.param_type is None
    assert param.default_value is False



