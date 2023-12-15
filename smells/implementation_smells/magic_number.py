import ast

from smells.smell_detector import ImplementationSmellDetector


def _create_smell(module, function_name, number, line):
    return {
        'module': module.name,
        'type': 'MagicNumber',
        'entity_name': function_name,
        'location': f"Line {line}",
        'details': f"Magic number {number} used in {function_name}."
    }


def _check_for_magic_numbers(module, entity, magic_numbers):
    smells = []
    for node in ast.walk(entity.ast_node):
        if isinstance(node, (ast.Num, ast.Constant)):  # Compatible with Python 3.8+
            num = node.n if isinstance(node, ast.Num) else (node.value if isinstance(node.value, (int, float)) else None)
            if num is not None and num not in magic_numbers:
                smells.append(_create_smell(module, entity.name, num, node.lineno))
    return smells


class MagicNumberDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        # Allow configuration of what numbers to ignore
        magic_numbers = set(config.get('threshold', range(0, 2)))
        # Check standalone functions and class methods
        for entity in module.functions + [m for c in module.classes for m in c.methods]:
            smells.extend(_check_for_magic_numbers(module, entity, magic_numbers))

        return smells
