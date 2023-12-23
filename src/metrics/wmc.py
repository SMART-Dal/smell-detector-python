import logging

from src.metrics import calculate_cyclomatic_complexity


def calculate_wmc_for_class(py_class):
    try:
        return sum(calculate_cyclomatic_complexity(method.ast_node) for method in py_class.methods)
    except Exception as e:
        logging.error(f"Error calculating WMC for class: {e}")
        return 0


def calculate_wmc_for_module(py_module):
    try:
        return sum(calculate_wmc_for_class(py_class) for py_class in py_module.classes)
    except Exception as e:
        logging.error(f"Error calculating WMC for module: {e}")
        return 0
