import ast

from ..smell_detector import ImplementationSmellDetector


class EmptyCatchBlockDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        for py_function in module.functions + [method for cls in module.classes for method in cls.methods]:
            smells.extend(self._check_for_empty_catch(module, py_function))
        return smells

    def _check_for_empty_catch(self, module, entity):
        smells = []
        for node in ast.walk(entity.ast_node):
            if isinstance(node, ast.Try):
                for handler in node.handlers:
                    if isinstance(handler, ast.ExceptHandler):
                        if not (handler.body and not isinstance(handler.body[0], ast.Pass)):
                            detail = f"Empty catch block found in {entity.name}."
                            smell_details = self._create_smell(module.name, entity, detail, handler.lineno)
                            smells.append(smell_details)
        return smells
