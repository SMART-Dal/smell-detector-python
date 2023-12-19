# test_sm_function.py
import pytest

from src.sourcemodel.sm_function import SMFunction


@pytest.fixture
def ast_node_mock(mocker):
    # Create a mock AST node using the mocker fixture from pytest-mock
    return mocker.MagicMock()


@pytest.fixture
def sm_function_instance(ast_node_mock):
    # Create an instance of SMFunction with mocked dependencies
    return SMFunction(name="TestFunction", start_line=1, end_line=10, ast_node=ast_node_mock)


def test_smfunction_initialization(sm_function_instance):
    assert sm_function_instance.name == "TestFunction"
    assert sm_function_instance.start_line == 1
    assert sm_function_instance.end_line == 10
    assert sm_function_instance.ast_node is not None


def test_add_parameter(sm_function_instance, mocker):
    # Use mocker to create a MagicMock
    param = mocker.MagicMock()
    sm_function_instance.add_parameter(param)
    assert param in sm_function_instance.parameters


def test_set_return_type(sm_function_instance):
    sm_function_instance.set_return_type("int")
    assert sm_function_instance.return_type == "int"


def test_add_body_statement(sm_function_instance, mocker):
    statement = mocker.MagicMock()
    sm_function_instance.add_body_statement(statement)
    assert statement in sm_function_instance.function_body


def test_add_local_variable(sm_function_instance):
    variable = "local_var"
    sm_function_instance.add_local_variable(variable)
    assert variable in sm_function_instance.local_variables


def test_add_called_method(sm_function_instance):
    method_name = "calledMethod"
    sm_function_instance.add_called_method(method_name)
    assert method_name in sm_function_instance.called_methods


def test_add_external_call(sm_function_instance):
    call_name = "externalCall"
    sm_function_instance.add_external_call(call_name)
    assert call_name in sm_function_instance.external_calls


def test_set_metrics(sm_function_instance):
    loc, complexity, parameter_count = 100, 10, 5
    sm_function_instance.set_metrics(loc, complexity, parameter_count)
    assert sm_function_instance.loc == loc
    assert sm_function_instance.complexity == complexity
    assert sm_function_instance.parameter_count == parameter_count
