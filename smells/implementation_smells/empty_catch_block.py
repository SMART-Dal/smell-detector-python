import ast

from ..smell_detector import ImplementationSmellDetector


def _create_smell(module,entity, handler):
    return {
        'module': module.name,
        'type': 'EmptyCatchBlock',
        'entity_name': entity.name,
        'location': f"Line {handler.lineno}",
        'details': f"Empty catch block found in {entity.name}."
    }


def _check_for_empty_catch(module,entity):
    smells = []
    for node in ast.walk(entity.ast_node):
        if isinstance(node, ast.Try):
            for handler in node.handlers:
                if isinstance(handler, ast.ExceptHandler):
                    if not (handler.body and not isinstance(handler.body[0], ast.Pass)):
                        smell_details = _create_smell(module,entity, handler)
                        smells.append(smell_details)
    return smells


class EmptyCatchBlockDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        print("Empty Catch Block Detector")
        for py_function in module.functions + [method for cls in module.classes for method in cls.methods]:
            smells.extend(_check_for_empty_catch(module, py_function))
        return smells
