import ast
import logging

from .cc import cyclomatic_complexity
from log_config import setup_logging

setup_logging()


def weighted_methods_per_class(node: ast.AST) -> int:
    if not isinstance(node, ast.ClassDef):
        return 0

    logging.info(f"Calculating weighted methods for class: {node.name}")
    total_complexity = 0
    for method_node in node.body:
        if isinstance(method_node, ast.FunctionDef):
            complexity = cyclomatic_complexity(method_node)
            logging.debug(f"Cyclomatic complexity for method {method_node.name}: {complexity}")
            total_complexity += complexity

    logging.debug(f"Total weighted methods for class {node.name}: {total_complexity}")
    return total_complexity
