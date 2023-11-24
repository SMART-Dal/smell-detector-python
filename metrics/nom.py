import ast
import logging

from log_config import setup_logging

setup_logging()


def number_of_methods(node: ast.AST) -> int:
    logging.info("Calculating number of methods in a class")
    if not isinstance(node, ast.ClassDef):
        return 0
    return sum(1 for item in node.body if isinstance(item, ast.FunctionDef))


def number_of_public_methods(node: ast.AST) -> int:
    logging.info("Calculating number of public methods in a class")
    if not isinstance(node, ast.ClassDef):
        return 0
    return sum(1 for item in node.body if isinstance(item, ast.FunctionDef) and not item.name.startswith("_"))
