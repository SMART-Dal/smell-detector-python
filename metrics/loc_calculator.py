# Calculate the total LOC for a module.
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
