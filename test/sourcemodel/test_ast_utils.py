import ast

from sourcemodel.ast_utils import get_return_type, get_function_body_and_variables, determine_access_modifier, \
    get_decorators, get_annotation, extract_package_name


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


def test_determine_access_modifier():
    public_func = ast.FunctionDef(name='public_function')
    private_func = ast.FunctionDef(name='_private_function')
    assert determine_access_modifier(public_func) == 'public'
    assert determine_access_modifier(private_func) == 'private'


def test_get_decorators():
    func_def = ast.FunctionDef(decorator_list=[ast.Name(id='decorator1'), ast.Name(id='decorator2')])
    assert get_decorators(func_def) == ['decorator1', 'decorator2']


def test_get_annotation():
    assert get_annotation(ast.Name(id='int')) == 'int'
    assert get_annotation(ast.Subscript(value=ast.Name(id='List'), slice=ast.Name(id='int'))) == 'List[int]'
    assert get_annotation(ast.Tuple(elts=[ast.Name(id='int'), ast.Name(id='str')])) == '(int, str)'


