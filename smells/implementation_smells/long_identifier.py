from ..smell_detector import ImplementationSmellDetector


def _create_smell_detail(module_name, name, line, entity_type):
    return {
        'module': module_name,
        'type': 'LongIdentifier',
        'entity_name': name,
        'location': f"Line {line}",
        'details': f"{entity_type} name '{name}' is too long."
    }


class LongIdentifierDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        module_name = module.name
        max_length = config.get("threshold")

        # Check for long class names
        for py_class in module.classes:
            if len(py_class.name) > max_length:

                smells.append(_create_smell_detail(module_name, py_class.name, py_class.start_line, 'Class'))

        # Check for long function/method names
        for py_function in module.functions + [method for cls in module.classes for method in cls.methods]:
            if len(py_function.name) > max_length:
                smells.append(_create_smell_detail(module_name, py_function.name, py_function.start_line, 'Function/Method'))

        return smells
