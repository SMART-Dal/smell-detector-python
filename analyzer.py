import ast
import logging
from metrics import cc, loc, nof, nom, pc, wmc
from log_config import setup_logging
from metrics.lcom3 import calculate_lcom3

setup_logging()


def analyze_node(node):
    if isinstance(node, ast.ClassDef):
        return {
            'type': 'class',
            'name': node.name,
            'number_of_fields': nof.number_of_fields(node),
            'number_of_methods': nom.number_of_methods(node),
            'wmc': wmc.weighted_methods_per_class(node),
            'loc': loc.class_loc(node),
            'lcom3': calculate_lcom3(node)
        }
    elif isinstance(node, ast.FunctionDef):
        return {
            'type': 'function',
            'name': node.name,
            'cyclomatic_complexity': cc.cyclomatic_complexity(node),
            'parameter_count': pc.parameter_count(node),
            'loc': loc.method_loc(node)
        }
    return None


def analyze_code(file_path):
    logging.info(f"Starting analysis of the file: {file_path}")
    try:
        with open(file_path, 'r') as file:
            node = ast.parse(file.read())

        metrics_data = []
        for n in ast.walk(node):
            result = analyze_node(n)
            if result:
                metrics_data.append(result)

        logging.info("Successfully completed analysis")
        return metrics_data

    except Exception as e:
        logging.error(f"Error occurred during analysis: {e}", exc_info=True)
        raise
