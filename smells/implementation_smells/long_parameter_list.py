from ..smell_detector import ImplementationSmellDetector


def _create_smell(module_name, entity, max_params):
    return {
        'module': module_name,
        'type': 'LongParameterList',
        'entity_name': entity.name,
        'location': f"Line {entity.start_line} - {entity.end_line}",
        'details': f"{entity.name} has {entity.parameter_count} parameters, exceeding the max of {max_params}"
    }


class LongParameterListDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        max_params = config.get("threshold")

        for py_class in module.classes:
            for method in py_class.methods:
                if method.parameter_count > max_params:
                    smells.append(_create_smell(module.name, method, max_params))

        for function in module.functions:
            if function.parameter_count > max_params:
                smells.append(_create_smell(module.name, function, max_params))

        return smells
