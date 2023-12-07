import ast


def get_return_type(node):
    if node.returns:
        return get_annotation(node.returns)
    return None


def get_function_body_and_variables(node):
    function_body = []
    local_variables = []
    for stmt in node.body:
        function_body.append(stmt)
        if isinstance(stmt, ast.Assign):
            for target in stmt.targets:
                if isinstance(target, ast.Name):
                    local_variables.append(target.id)
    return function_body, local_variables


def determine_access_modifier(node):
    if node.name.startswith('_'):
        return 'private'
    return 'public'


def get_decorators(node):
    return [decorator.id for decorator in node.decorator_list if isinstance(decorator, ast.Name)]


def get_annotation(annotation):
    if isinstance(annotation, ast.Name):
        return annotation.id
    elif isinstance(annotation, ast.Subscript):
        return f"{get_annotation(annotation.value)}[{get_annotation(annotation.slice)}]"
    elif isinstance(annotation, ast.Index):
        return get_annotation(annotation.value)
    elif isinstance(annotation, ast.Tuple):
        return f"({', '.join(get_annotation(elt) for elt in annotation.elts)})"
    # Add more cases as needed for complex annotations
    return "complex_type"
