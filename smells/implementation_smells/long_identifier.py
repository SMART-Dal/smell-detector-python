from ..smell_detector import ImplementationSmellDetector


def _create_smell(module_name, entity, line, entity_type):
    return {
        'module': module_name,
        'type': 'LongIdentifier',
        'entity_name': entity.name,
        'location': f"Line {line}",
        'details': f"{entity_type} name '{entity.name}' is too long."
    }


class LongIdentifierDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        max_length = config.get("threshold")

        # Check for long class names
        for py_class in module.classes:
            if len(py_class.name) > max_length:

                smells.append(_create_smell(module.name, py_class, py_class.start_line, 'Class'))

        # Check for long function/method names
        for py_function in module.functions + [method for cls in module.classes for method in cls.methods]:
            if len(py_function.name) > max_length:
                smells.append(_create_smell(module.name, py_function, py_function.start_line, 'Function/Method'))

        return smells
