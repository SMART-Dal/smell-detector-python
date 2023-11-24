import ast
import logging

from log_config import setup_logging

setup_logging()


def method_loc(node: ast.AST) -> int:
    logging.info("Calculating LOC for method")
    if isinstance(node, ast.FunctionDef):
        return node.end_lineno - node.lineno + 1
    return 0


def class_loc(node: ast.AST) -> int:
    logging.info("Calculating LOC for class")
    if isinstance(node, ast.ClassDef):
        start_line = node.lineno
        end_line = max(child.lineno for child in ast.walk(node) if hasattr(child, 'lineno'))
        return end_line - start_line + 1
    return 0
