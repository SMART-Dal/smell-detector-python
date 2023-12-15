import ast
from ..smell_detector import ImplementationSmellDetector


def _create_smell(module_name, entity, node, complexity, max_operators):
    return {
        'module': module_name,
        'type': 'ComplexConditional',
        'entity_name': entity.name,
        'location': f"Line {node.lineno}",
        'details': f"A conditional in {entity.name} has a complexity of {complexity}, exceeding the max of {max_operators}."
    }


def _count_logical_operators(node):
    # Count the number of logical operators in a conditional expression
    count = 0
    for child in ast.walk(node):
        if isinstance(child, (ast.And, ast.Or, ast.Not)):
            count += 1
    return count


class ComplexConditionalDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        max_operators = config.get("threshold")

        for py_function in module.functions + [method for cls in module.classes for method in cls.methods]:
            # Visit each node in the function or method body
            for node in ast.walk(py_function.ast_node):
                if isinstance(node, (ast.If, ast.While, ast.BoolOp)):
                    complexity = _count_logical_operators(node)
                    if complexity > max_operators:
                        smell_detail = _create_smell(module.name, py_function, node, complexity, max_operators)
                        smells.append(smell_detail)

        return smells
