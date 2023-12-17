import ast
import logging

from ..smell_detector import ImplementationSmellDetector


class EmptyCatchBlockDetector(ImplementationSmellDetector):
    def _detect_smells(self, module, config):
        logging.debug(f"Starting empty catch block detection in module: {module.name}")
        smells = []
        try:
            for py_function in module.functions + [method for cls in module.classes for method in cls.methods]:
                smells.extend(self._check_for_empty_catch(module, py_function))
        except Exception as e:
            logging.error(f"Error during smell detection in module {module.name}: {e}", exc_info=True)
            return []

        logging.debug(f"Completed empty catch block detection in module: {module.name}")
        return smells

    def _check_for_empty_catch(self, module, entity):
        smells = []
        try:
            for node in ast.walk(entity.ast_node):
                if isinstance(node, ast.Try):
                    for handler in node.handlers:
                        if isinstance(handler, ast.ExceptHandler):
                            if not (handler.body and not isinstance(handler.body[0], ast.Pass)):
                                detail = f"Empty catch block found in {entity.name}."
                                smell_details = self._create_smell(module.name, entity, detail, handler.lineno)
                                smells.append(smell_details)
        except Exception as e:
            logging.error(f"Error checking for empty catch blocks in {entity.name} of module {module.name}: {e}",
                          exc_info=True)

        logging.info(
            f"Completed empty catch block detection in module: {module.name}. Total smells detected: {len(smells)}")
        return smells
