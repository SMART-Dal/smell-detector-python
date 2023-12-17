from ..smell_detector import ImplementationSmellDetector


class LongParameterListDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        max_params = config.get("threshold")

        for entity in self._iterate_functions_and_methods(module):
            if entity.parameter_count > max_params:
                detail = f"{entity.name} has {entity.parameter_count} parameters, exceeding the max of {max_params}."
                location = f"{entity.start_line} - {entity.end_line}"
                smells.append(self._create_smell(module.name, entity, detail, location))

        return smells
