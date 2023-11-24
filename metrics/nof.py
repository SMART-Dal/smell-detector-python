import ast
import logging

from log_config import setup_logging

setup_logging()


def number_of_fields(node: ast.AST) -> int:
    logging.info("Calculating number of fields in a class")
    if not isinstance(node, ast.ClassDef):
        return 0
    return sum(
        1 for item in node.body
        if isinstance(item, ast.Assign)
        and any(isinstance(target, ast.Name) for target in item.targets)
    )


def number_of_public_fields(node: ast.AST) -> int:
    logging.info("Calculating number of public fields in a class")
    if not isinstance(node, ast.ClassDef):
        return 0
    return sum(
        1 for item in node.body
        if isinstance(item, ast.Assign)
        and any(
            isinstance(target, ast.Name) and not target.id.startswith("_")
            for target in item.targets
        )
    )
