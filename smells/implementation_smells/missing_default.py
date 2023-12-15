import ast

from smells.smell_detector import ImplementationSmellDetector


def _has_else(node):
    # Recursively check for an else block in the if-elif-else chain
    current = node
    while True:
        if not current.orelse:
            return False
        elif len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
            current = current.orelse[0]
        else:
            return True


def _has_missing_default(node):
    # Traverse the AST to find if-elif-else chains
    for child in ast.walk(node):
        if isinstance(child, ast.If):
            # Check if this 'if' node is part of an if-elif-else chain without a default (else) case
            if not _has_else(child):
                return True
    return False


def _create_smell(module_name, entity):
    return {
        'module': module_name,
        'type': 'MissingDefault',
        'entity_name': entity.name,
        'location': f"Line {entity.start_line}",
        'details': f"Missing default case in {entity.name}."
    }


class MissingDefaultDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        # Check standalone functions and class methods
        for entity in module.functions + [m for c in module.classes for m in c.methods]:
            if _has_missing_default(entity.ast_node):
                smells.append(_create_smell(module.name, entity))
        return smells
