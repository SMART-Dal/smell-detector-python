import ast
import logging

from ..smell_detector import ImplementationSmellDetector


class MagicNumberDetector(ImplementationSmellDetector):
    def _detect_smells(self, module, config):
        logging.info(f"Starting magic number detection in module: {module.name}")
        smells = []
        magic_numbers = set(config.get('threshold', range(0, 2)))  # Allow configuration of what numbers to ignore

        for entity in self._iterate_functions_and_methods(module):
            try:
                smells.extend(self._check_for_magic_numbers(module, entity, magic_numbers))
            except Exception as e:
                logging.error(f"Error analyzing {entity.name} in {module.name}: {e}", exc_info=True)

        logging.info(f"Completed magic number detection in module: {module.name}. Total smells detected: {len(smells)}")
        return smells

    def _check_for_magic_numbers(self, module, entity, magic_numbers):
        smells = []
        for node in ast.walk(entity.ast_node):
            try:
                if isinstance(node, (ast.Num, ast.Constant)):  # Compatible with Python 3.8+
                    num = node.n if isinstance(node, ast.Num) else (
                        node.value if isinstance(node.value, (int, float)) else None)
                    if num is not None and num not in magic_numbers:
                        detail = f"Magic number {num} used in {entity.name}."
                        smells.append(self._create_smell(module.name, entity, detail, node.lineno))
                        logging.debug(f"Magic number {num} detected in {entity.name} at line {node.lineno} in {module.name}")
            except Exception as e:
                logging.error(f"Error processing node in {entity.name} of {module.name}: {e}", exc_info=True)

        return smells
