# import logging


# def calculate_parameter_count(py_function):
#     try:
#         return len(py_function.parameters)
#     except AttributeError as e:
#         logging.error(f"Invalid function object provided for parameter count calculation: {e}")
#         return 0

import logging

def calculate_parameter_count(py_function):
    try:
        param_count = len(py_function.parameters)
        # Exclude "self" parameter if it's present
        for parameter in py_function.parameters:
            if parameter.name == "self":
                param_count -= 1
                break
        return param_count
    except AttributeError as e:
        logging.error(f"Invalid function object provided for parameter count calculation: {e}")
        return 0
