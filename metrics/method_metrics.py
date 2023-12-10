# Calculate the total LOC for a module.
import ast


def calculate_module_loc(py_module):
    total_lines = 0
    for py_class in py_module.classes:
        total_lines += calculate_class_loc(py_class)
    for py_function in py_module.functions:
        total_lines += calculate_function_loc(py_function)
    return total_lines


# Calculate the LOC for a class.
def calculate_class_loc(py_class):
    return py_class.end_line - py_class.start_line + 1


# Calculate the LOC for a function or method.
def calculate_function_loc(py_function):
    return py_function.end_line - py_function.start_line + 1


def calculate_cyclomatic_complexity(node):
    complexity = 1
    for child in ast.walk(node):
        if isinstance(child, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.ExceptHandler)):
            complexity += 1
    return complexity


def calculate_parameter_count(py_function):
    return len(py_function.parameters)

