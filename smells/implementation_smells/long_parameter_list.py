from ..smell_detector import ImplementationSmellDetector


def create_smell_detail(module_name, entity, param_count, max_params):
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
        module_name = module.name
        max_params = config.get("threshold")

        for py_class in module.classes:
            for method in py_class.methods:
                if len(method.parameters) > max_params:
                    smells.append(create_smell_detail(module_name, method, len(method.parameters), max_params))

        for function in module.functions:
            if len(function.parameters) > max_params:
                smells.append(create_smell_detail(module_name, function, len(function.parameters), max_params))

        return smells
