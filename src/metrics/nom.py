import logging


def calculate_nom(py_class):
    try:
        return len(py_class.methods)
    except AttributeError as e:
        logging.error(f"Invalid class object provided for NOM calculation: {e}")
        return 0


def calculate_nopm(py_class):
    try:
        return sum(1 for method in py_class.methods if not method.name.startswith('_'))
    except AttributeError as e:
        logging.error(f"Invalid class object provided for NOPM calculation: {e}")
        return 0
