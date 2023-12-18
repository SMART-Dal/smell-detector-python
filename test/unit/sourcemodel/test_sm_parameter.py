import pytest
from src.sourcemodel.sm_parameter import PyParameter


@pytest.fixture
def parameter_data():
    return {
        "name": "param1",
        "param_type": "int",
        "default_value": 10
    }


def test_pyparameter_initialization(parameter_data):
    param = PyParameter(**parameter_data)
    assert param.name == parameter_data['name'], "The name should be initialized correctly"
    assert param.param_type == parameter_data['param_type'], "The param_type should be initialized correctly"
    assert param.default_value == parameter_data['default_value'], "The default_value should be initialized correctly"


def test_pyparameter_default_values():
    param = PyParameter(name="param2")
    assert param.name == "param2", "The name should be initialized correctly"
    assert param.param_type is None, "The param_type should be None by default"
    assert param.default_value is None, "The default_value should be None by default"
