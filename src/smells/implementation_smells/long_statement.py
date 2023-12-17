import logging

import astunparse

from ..smell_detector import ImplementationSmellDetector


def _ast_to_string(node):
    try:
        return astunparse.unparse(node).strip()
    except Exception as e:
        logging.error(f"Failed to convert AST node to string: {e}", exc_info=True)
        return "<error in AST conversion>"


class LongStatementDetector(ImplementationSmellDetector):
    def _detect_smells(self, module, config):
        logging.info(f"Starting long statement detection in module: {module.name}")
        smells = []
        max_length = config.get("threshold", 100)  # Default to 100 if not specified

        for entity in self._iterate_functions_and_methods(module):
            try:
                for statement in entity.function_body:
                    statement_str = _ast_to_string(statement)
                    if len(statement_str) > max_length:
                        detail = f"A statement with {len(statement_str)} chars in {entity.name} exceeds the maximum length of {max_length} characters."
                        smells.append(self._create_smell(module.name, entity, detail, statement.lineno))
                        logging.info(
                            f"Long statement ({len(statement_str)} chars) detected in {entity.name} at line {statement.lineno} in {module.name}")
            except Exception as e:
                logging.error(f"Error analyzing {entity.name} in {module.name}: {e}", exc_info=True)

        logging.info(
            f"Completed long statement detection in module: {module.name}. Total smells detected: {len(smells)}")
        return smells
