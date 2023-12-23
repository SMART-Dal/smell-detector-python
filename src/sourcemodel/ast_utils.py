import ast
import os


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


def extract_package_name(file_path, project_root):
    directory = os.path.dirname(file_path)
    package_parts = []

    # Traverse up until the project root or filesystem root
    while directory and (project_root is None or directory.startswith(project_root)):
        directory, package_part = os.path.split(directory)
        if package_part:  # Ignore empty parts
            package_parts.append(package_part)

    package_name = '.'.join(reversed(package_parts))
    return package_name
