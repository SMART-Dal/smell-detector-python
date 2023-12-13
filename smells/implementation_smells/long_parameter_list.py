from ..smell_detector import ImplementationSmellDetector


def _create_smell(module_name, entity, param_count, max_params):
    return {
        'module': module_name,
        'type': 'LongParameterList',
        'entity_name': entity.name,
        'location': f"Line {entity.start_line} - {entity.end_line}",
        'details': f"{entity.name} has {param_count} parameters, exceeding the max of {max_params}"
    }


class LongParameterListDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        max_params = config.get("threshold")

        for py_class in module.classes:
            for method in py_class.methods:
                if len(method.parameters) > max_params:
                    smells.append(_create_smell(module.name, method, len(method.parameters), max_params))

        for function in module.functions:
            if len(function.parameters) > max_params:
                smells.append(_create_smell(module.name, function, len(function.parameters), max_params))

        return smells
