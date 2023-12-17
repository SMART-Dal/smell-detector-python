import ast
import logging

from ..smell_detector import ImplementationSmellDetector


def _has_else(node):
    try:
        current = node
        while True:
            if not current.orelse:
                return False
            elif len(current.orelse) == 1 and isinstance(current.orelse[0], ast.If):
                current = current.orelse[0]
            else:
                return True
    except Exception as e:
        logging.error(f"Error checking for else block: {e}", exc_info=True)
        return False


def _has_missing_default(node):
    try:
        for child in ast.walk(node):
            if isinstance(child, ast.If) and not _has_else(child):
                return True
        return False
    except Exception as e:
        logging.error(f"Error checking for missing default: {e}", exc_info=True)
        return False


class MissingDefaultDetector(ImplementationSmellDetector):
    def _detect_smells(self, module, config):
        logging.info(f"Starting missing default case detection in module: {module.name}")
        smells = []

        for entity in self._iterate_functions_and_methods(module):
            try:
                if _has_missing_default(entity.ast_node):
                    detail = f"Missing default case in {entity.name}."
                    smells.append(self._create_smell(module.name, entity, detail, entity.start_line))
                    logging.debug(f"Missing default case detected in {entity.name} in {module.name}")
            except Exception as e:
                logging.error(f"Error analyzing {entity.name} in {module.name}: {e}", exc_info=True)

        logging.info(
            f"Completed missing default case detection in module: {module.name}. Total smells detected: {len(smells)}")
        return smells
