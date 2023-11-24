import ast
import logging

from log_config import setup_logging

setup_logging()


def cyclomatic_complexity(node: ast.AST) -> int:
    logging.info("Calculating cyclomatic complexity")
    if not isinstance(node, ast.FunctionDef):
        return 0

    complexity = 1
    for item in ast.walk(node):
        if isinstance(item, (ast.If, ast.While, ast.For, ast.And, ast.Or, ast.BoolOp)):
            complexity += 1
    return complexity
