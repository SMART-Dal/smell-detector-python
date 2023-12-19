import ast
import pytest

from src.sourcemodel import ast_utils

# Sample data for testing
sample_function_code = """
def sample_function(param1: int, param2: int) -> int:
    var = param1 + param2
    return var
"""


@pytest.fixture
def sample_ast_function():
    return ast.parse(sample_function_code).body[0]


# Test get_return_type
def test_get_return_type(sample_ast_function):
    assert ast_utils.get_return_type(sample_ast_function) == 'int', "Should correctly identify return type annotation"


# Test get_function_body_and_variables
def test_get_function_body_and_variables(sample_ast_function):
    body, variables = ast_utils.get_function_body_and_variables(sample_ast_function)
    assert len(body) == 2, "Should correctly identify the number of statements in the function body"
    assert 'var' in variables, "Should correctly identify local variables"


# Test get_decorators
def test_get_decorators_with_decorators(mocker):
    # Mocking a function with decorators
    func_node = mocker.MagicMock(spec=ast.FunctionDef)
    decorator_list = [mocker.MagicMock(spec=ast.Name) for _ in range(2)]
    for deco, name in zip(decorator_list, ['deco1', 'deco2']):
        deco.id = name
    func_node.decorator_list = decorator_list
    assert set(ast_utils.get_decorators(func_node)) == {'deco1', 'deco2'}, "Should correctly identify decorators"


# Test get_annotation for complex types
@pytest.mark.parametrize("annotation, expected", [
    (ast.Name(id='int'), 'int'),
    (ast.Subscript(value=ast.Name(id='List'), slice=ast.Index(value=ast.Name(id='int'))), 'List[int]'),
    (ast.Tuple(elts=[ast.Name(id='int'), ast.Name(id='str')]), '(int, str)')
])
def test_get_annotation(annotation, expected):
    assert ast_utils.get_annotation(annotation) == expected, f"Should correctly interpret {expected} annotation"


# Test extract_package_name
def test_extract_package_name(mocker):
    mocker.patch('os.path.dirname', return_value='/path/to/module')
    mocker.patch('os.path.split', side_effect=[('/path/to', 'module'), ('/path', 'to'), ('/', '')])
    assert ast_utils.extract_package_name('/path/to/module/file.py',
                                          '/path') == 'to.module', "Should correctly extract package name"


# Add tests for error handling
def test_get_annotation_with_unsupported_type(mocker):
    complex_node = mocker.MagicMock(spec=ast.AST)
    assert ast_utils.get_annotation(
        complex_node) == "complex_type", "Should handle unsupported annotation types gracefully"
