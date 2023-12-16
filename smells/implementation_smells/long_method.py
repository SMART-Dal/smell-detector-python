from ..smell_detector import ImplementationSmellDetector


class LongMethodDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        max_lines = config.get("threshold")

        for entity in self._iterate_functions_and_methods(module):
            if entity.loc > max_lines:
                detail = f"Method '{entity.name}' is too long ({entity.loc} lines)."
                location = f"{entity.start_line} - {entity.end_line}"
                smells.append(self._create_smell(module.name, entity, detail, location))

        return smells
