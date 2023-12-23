import logging


def calculate_module_loc(py_module):
    try:
        total_lines = 0
        for py_class in py_module.classes:
            total_lines += calculate_class_loc(py_class)
        for py_function in py_module.functions:
            total_lines += calculate_function_loc(py_function)
        return total_lines
    except AttributeError as e:
        logging.error(f"Invalid module object provided: {e}")
        return 0


def calculate_class_loc(py_class):
    try:
        return py_class.end_line - py_class.start_line + 1
    except AttributeError as e:
        logging.error(f"Invalid class object provided: {e}")
        return 0


def calculate_function_loc(py_function):
    try:
        return py_function.end_line - py_function.start_line + 1
    except AttributeError as e:
        logging.error(f"Invalid function object provided: {e}")
        return 0
