import ast

from smells.smell_detector import ImplementationSmellDetector


class MagicNumberDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        # Allow configuration of what numbers to ignore
        magic_numbers = set(config.get('threshold', range(0, 2)))
        # Check standalone functions and class methods
        for entity in self._iterate_functions_and_methods(module):
            smells.extend(self._check_for_magic_numbers(module, entity, magic_numbers))

        return smells

    def _check_for_magic_numbers(self, module, entity, magic_numbers):
        smells = []
        for node in ast.walk(entity.ast_node):
            if isinstance(node, (ast.Num, ast.Constant)):  # Compatible with Python 3.8+
                num = node.n if isinstance(node, ast.Num) else (
                    node.value if isinstance(node.value, (int, float)) else None)
                if num is not None and num not in magic_numbers:
                    details = f"Magic number {num} used in {entity.name}."
                    smells.append(self._create_smell(module.name, entity, details, node.lineno))
        return smells
