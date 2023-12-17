import logging


def calculate_nof(py_class):
    try:
        return len(py_class.class_fields)
    except AttributeError as e:
        logging.error(f"Invalid class object provided for NOF calculation: {e}")
        return 0


def calculate_nopf(py_class):
    try:
        return sum(1 for _, access in py_class.class_fields.items() if access == 'public')
    except AttributeError as e:
        logging.error(f"Invalid class object provided for NOPF calculation: {e}")
        return 0


def calculate_module_nof(py_module):
    try:
        return len(py_module.global_variables)
    except AttributeError as e:
        logging.error(f"Invalid module object provided for module NOF calculation: {e}")
        return 0


def calculate_module_nopf(py_module):
    try:
        return sum(1 for var in py_module.global_variables if not var.startswith('_'))
    except AttributeError as e:
        logging.error(f"Invalid module object provided for module NOPF calculation: {e}")
        return 0
