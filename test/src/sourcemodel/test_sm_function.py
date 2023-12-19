import pytest
from pytest_mock import mocker

from src.sourcemodel.sm_function import SMFunction
from src.sourcemodel.sm_parameter import SMParameter


# Fixture for creating a standard SMFunction instance
@pytest.fixture
def sm_function_instance(mocker):
    ast_node_mock = mocker.MagicMock()  # Replace with an actual AST node if needed
    return SMFunction(name="testFunction", start_line=1, end_line=10, ast_node=ast_node_mock)


# Fixture for creating a mock parameter object
@pytest.fixture
def parameter_mock(mocker):
    return mocker.MagicMock(spec=SMParameter, name="test_parameter")


# Testing the initialization and basic properties of SMFunction
def test_smfunction_initialization(sm_function_instance):
    assert sm_function_instance.name == "testFunction", "The name should be initialized correctly"
    assert sm_function_instance.start_line == 1, "The start line should be initialized correctly"
    assert sm_function_instance.end_line == 10, "The end line should be initialized correctly"
    assert sm_function_instance.parameters == [], "Parameters should be initialized to an empty list"


# Testing the addition of parameters to the function
def test_add_parameter(sm_function_instance, parameter_mock):
    sm_function_instance.add_parameter(parameter_mock)
    assert parameter_mock in sm_function_instance.parameters, "The parameter should be added to the function"


# Testing the setting of the return type
def test_set_return_type(sm_function_instance):
    return_type = "int"
    sm_function_instance.set_return_type(return_type)
    assert sm_function_instance.return_type == return_type, "The return type should be set correctly"


# Testing the addition of body statements to the function
def test_add_body_statement(sm_function_instance):
    statement = "print('hello world')"
    sm_function_instance.add_body_statement(statement)
    assert statement in sm_function_instance.function_body, "The statement should be added to the function body"


# Testing the addition of local variables
def test_add_local_variable(sm_function_instance):
    variable = "localVar"
    sm_function_instance.add_local_variable(variable)
    assert variable in sm_function_instance.local_variables, "The local variable should be added"


# Testing the registration of called methods and used modules
def test_add_called_method(sm_function_instance):
    method_name = "someModule.someMethod"
    sm_function_instance.add_called_method(method_name)
    assert method_name in sm_function_instance.called_methods, "The called method should be registered"
    assert "someModule" in sm_function_instance.used_modules, "The used module should be registered"


# Testing the registration of external calls
def test_add_external_call(sm_function_instance):
    called_name = "externalFunction()"
    sm_function_instance.add_external_call(called_name)
    assert called_name in sm_function_instance.external_calls, "The external call should be registered"


# Testing the setting of metrics
def test_set_metrics(sm_function_instance):
    loc, complexity, parameter_count = 10, 5, 3
    sm_function_instance.set_metrics(loc, complexity, parameter_count)
    assert sm_function_instance.loc == loc, "LOC should be set correctly"
    assert sm_function_instance.complexity == complexity, "Complexity should be set correctly"
    assert sm_function_instance.parameter_count == parameter_count, "Parameter count should be set correctly"
