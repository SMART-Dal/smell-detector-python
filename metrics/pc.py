import ast
import logging

from log_config import setup_logging

setup_logging()


def parameter_count(node: ast.AST) -> int:
    logging.info(f"Calculating parameter count for node: {ast.dump(node)}")
    if isinstance(node, ast.FunctionDef):
        count = len(node.args.args)
        logging.debug(f"Parameter count for {node.name}: {count}")
        return count
    return 0
