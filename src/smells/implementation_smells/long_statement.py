import astunparse
from ..smell_detector import ImplementationSmellDetector


def _ast_to_string(node):
    # Convert an AST node to its string representation using astunparse
    return astunparse.unparse(node).strip()


# def _create_smell_detail(module_name, entity, statement, max_length):
#     return {
#         'module': module_name,
#         'type': 'LongStatement',
#         'entity_name': entity.name,
#         'location': f"Line {statement.lineno}",
#         'details': f"A statement in {entity.name} exceeds the maximum length of {max_length} characters."
#     }


class LongStatementDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        max_length = config.get("threshold")

        for entity in self._iterate_functions_and_methods(module):
            for statement in entity.function_body:
                statement_str = _ast_to_string(statement)
                if len(statement_str) > max_length:
                    detail = f"A statement in {entity.name} exceeds the maximum length of {max_length} characters."
                    smells.append(self._create_smell(module.name, entity, detail, statement.lineno))

        return smells

        # for py_function in module.functions + [method for cls in module.classes for method in cls.methods]:
        #     for statement in py_function.function_body:
        #         statement_str = _ast_to_string(statement)
        #         if len(statement_str) > max_length:
        #             smell_detail = _create_smell_detail(module.name, py_function, statement, max_length)
        #             smells.append(smell_detail)

        # return smells
