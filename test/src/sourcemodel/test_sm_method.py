import pytest
from src.sourcemodel.sm_method import SMMethod


# Test the initialization of SMMethod
def test_sm_method_initialization(mocker):
    name = "method_name"
    start_line = 10
    end_line = 20
    access_modifier = "public"
    decorators = ["@decorator1", "@decorator2"]
    ast_node_mock = mocker.MagicMock()  # Replace with an actual AST node if needed

    sm_method = SMMethod(name, start_line, end_line, access_modifier, decorators, ast_node_mock)

    # Assert that the SMMethod is correctly initialized
    assert sm_method.name == name, "Name should be set correctly"
    assert sm_method.start_line == start_line, "Start line should be set correctly"
    assert sm_method.end_line == end_line, "End line should be set correctly"
    assert sm_method.access_modifier == access_modifier, "Access modifier should be set correctly"
    assert sm_method.decorators == decorators, "Decorators should be set correctly"
    assert sm_method.ast_node == ast_node_mock, "AST node should be set correctly"

