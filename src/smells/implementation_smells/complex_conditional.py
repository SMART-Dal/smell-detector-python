import ast
from ..smell_detector import ImplementationSmellDetector


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

        for entity in self._iterate_functions_and_methods(module):
            # Visit each node in the function or method body
            for node in ast.walk(entity.ast_node):
                if isinstance(node, (ast.If, ast.While, ast.BoolOp)):
                    complexity = _count_logical_operators(node)
                    if complexity > max_operators:
                        detail = f"A conditional in {entity.name} has a complexity of {complexity}, exceeding the max of {max_operators}."
                        smell_detail = self._create_smell(module.name, entity, detail, node.lineno)
                        smells.append(smell_detail)

        return smells
