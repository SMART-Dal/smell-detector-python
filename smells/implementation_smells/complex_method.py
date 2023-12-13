from ..smell_detector import ImplementationSmellDetector


def _create_smell(module_name, entity, max_complexity):
    return {
        'module': module_name,
        'type': 'ComplexMethod',
        'entity_name': entity.name,
        'location': f"Line {entity.start_line} - {entity.end_line}",
        'details': f"Method '{entity.name}' has a cyclomatic complexity of {entity.complexity}, exceeding the max of {max_complexity}."
    }


class ComplexMethodDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        max_complexity = config.get("threshold")

        # Check complexity in class methods
        for py_class in module.classes:
            for method in py_class.methods:
                if method.complexity > max_complexity:
                    smells.append(_create_smell(module.name, method, max_complexity))

        # Check complexity in standalone functions
        for function in module.functions:
            if function.complexity > max_complexity:
                smells.append(_create_smell(module.name, function, max_complexity))

        return smells
