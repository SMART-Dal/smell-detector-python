from ..smell_detector import ImplementationSmellDetector


class ComplexMethodDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        max_complexity = config.get("threshold")

        for entity in self._iterate_functions_and_methods(module):
            if entity.complexity > max_complexity:
                detail = f"Method '{entity.name}' has a cyclomatic complexity of {entity.complexity}, exceeding the max of {max_complexity}."
                location = f"{entity.start_line} - {entity.end_line}"
                smells.append(self._create_smell(module.name, entity, detail, location))
        return smells
