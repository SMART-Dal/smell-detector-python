from ..smell_detector import ImplementationSmellDetector


class LongIdentifierDetector(ImplementationSmellDetector):
    def detect(self, module, config):
        smells = []
        max_length = config.get("threshold")

        # Check for long class names
        for py_class in module.classes:
            if len(py_class.name) > max_length:
                detail = f"Class '{py_class.name}' is too long."
                smells.append(self._create_smell(module.name, py_class, detail, py_class.start_line))

        for entity in self._iterate_functions_and_methods(module):
            if len(entity.name) > max_length:
                detail = f"Function/Method name '{entity.name}' is too long."
                smells.append(self._create_smell(module.name, entity, detail, entity.start_line))

        return smells
