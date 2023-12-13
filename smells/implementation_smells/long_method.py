from ..smell_detector import ImplementationSmellDetector


def _create_smell(module_name, entity, line_count):
    return {
        'module': module_name,
        'type': 'LongMethod',
        'entity_name': entity.name,
        'location': f"Line {entity.start_line} - {entity.end_line}",
        'details': f"Method '{entity.name}' is too long ({line_count} lines)."
    }


class LongMethodDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        max_lines = config.get("threshold")

        # Check for long methods in classes
        for py_class in module.classes:
            for method in py_class.methods:
                if method.loc > max_lines:
                    smells.append(_create_smell(module.name, method, method.loc))

        # Check for long standalone functions
        for function in module.functions:
            if function.loc > max_lines:
                smells.append(_create_smell(module.name, function, function.loc))

        return smells
