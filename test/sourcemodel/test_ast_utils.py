import ast

from sourcemodel.ast_utils import get_return_type, get_function_body_and_variables, \
    get_decorators, get_annotation


def test_get_return_type():
    func_def = ast.FunctionDef(returns=ast.Name(id='int', ctx=ast.Load()))
    assert get_return_type(func_def) == 'int'
    assert get_return_type(ast.FunctionDef()) is None


def test_get_function_body_and_variables():
    module = ast.parse("def foo():\n  x = 1\n  y = 2")
    func_def = module.body[0]
    body, variables = get_function_body_and_variables(func_def)

    assert len(body) == 2
    assert set(variables) == {'x', 'y'}


def test_get_annotation():
    assert get_annotation(ast.Name(id='int')) == 'int'
    assert get_annotation(ast.Subscript(value=ast.Name(id='List'), slice=ast.Name(id='int'))) == 'List[int]'
    assert get_annotation(ast.Tuple(elts=[ast.Name(id='int'), ast.Name(id='str')])) == '(int, str)'
