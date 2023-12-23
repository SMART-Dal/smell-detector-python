import pytest

from sourcemodel.sm_function import PyFunction


@pytest.fixture
def sample_pyfunction():
    return PyFunction("testFunction", 1, 5)


def test_pyfunction_initialization(sample_pyfunction):
    assert sample_pyfunction.name == "testFunction"
    assert sample_pyfunction.start_line == 1
    assert sample_pyfunction.end_line == 5
    assert sample_pyfunction.parameters == []
    assert sample_pyfunction.return_type is None
    assert sample_pyfunction.function_body == []
    assert sample_pyfunction.local_variables == []


def test_add_parameter(sample_pyfunction):
    sample_pyfunction.add_parameter("param1")
    assert "param1" in sample_pyfunction.parameters


def test_set_return_type(sample_pyfunction):
    sample_pyfunction.set_return_type("int")
    assert sample_pyfunction.return_type == "int"


def test_add_body_statement(sample_pyfunction):
    sample_pyfunction.add_body_statement("print('Hello')")
    assert "print('Hello')" in sample_pyfunction.function_body


def test_add_local_variable(sample_pyfunction):
    sample_pyfunction.add_local_variable("var1")
    assert "var1" in sample_pyfunction.local_variables


def test_function_body_integrity(sample_pyfunction):
    sample_pyfunction.add_body_statement("line1")
    sample_pyfunction.add_body_statement("line2")
    assert sample_pyfunction.function_body == ["line1", "line2"]


def test_local_variables_integrity(sample_pyfunction):
    sample_pyfunction.add_local_variable("var1")
    sample_pyfunction.add_local_variable("var2")
    assert sample_pyfunction.local_variables == ["var1", "var2"]

# Additional tests can be added as needed based on specific behaviors and requirements of your PyFunction implementation
