import logging


def calculate_fan_in_class(py_class):
    try:
        return len(py_class.method_interactions)
    except AttributeError as e:
        logging.error(f"Invalid class object provided: {e}")
        return 0


def calculate_fan_out_class(py_class):
    try:
        return len(py_class.external_dependencies)
    except AttributeError as e:
        logging.error(f"Invalid class object provided: {e}")
        return 0


def calculate_fan_in_module(py_module, dependency_graph):
    try:
        return dependency_graph.in_degree(py_module.name)
    except Exception as e:
        logging.error(f"Error calculating fan-in for module: {e}")
        return 0


def calculate_fan_out_module(py_module, dependency_graph):
    try:
        return dependency_graph.out_degree(py_module.name)
    except Exception as e:
        logging.error(f"Error calculating fan-out for module: {e}")
        return 0
