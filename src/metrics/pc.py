import logging


def calculate_parameter_count(py_function):
    try:
        return len(py_function.parameters)
    except AttributeError as e:
        logging.error(f"Invalid function object provided for parameter count calculation: {e}")
        return 0
