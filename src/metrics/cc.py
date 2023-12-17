import ast
import logging


def calculate_cyclomatic_complexity(node):
    if not isinstance(node, ast.AST):
        logging.error(f"Invalid input for cyclomatic complexity calculation: {node}")
        return 0

    complexity = 1
    try:
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.ExceptHandler)):
                complexity += 1
    except Exception as e:
        logging.error(f"Error calculating cyclomatic complexity: {e}")
        return 0
    return complexity
