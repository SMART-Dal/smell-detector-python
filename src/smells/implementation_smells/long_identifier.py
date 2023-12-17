import logging

from ..smell_detector import ImplementationSmellDetector


class LongIdentifierDetector(ImplementationSmellDetector):
    def _detect_smells(self, module, config):
        logging.debug(f"Starting long identifier detection in module: {module.name}")
        smells = []
        max_length = config.get("threshold", 30)  # Default to 30 if not specified

        try:
            # Check for long class names
            for py_class in module.classes:
                if len(py_class.name) > max_length:
                    detail = f"Class '{py_class.name}' exceeds the maximum length of {max_length} characters."
                    smells.append(self._create_smell(module.name, py_class, detail, py_class.start_line))

            # Check for long function/method names
            for entity in self._iterate_functions_and_methods(module):
                if len(entity.name) > max_length:
                    detail = f"Function/Method name '{entity.name}' exceeds the maximum length of {max_length} characters."
                    smells.append(self._create_smell(module.name, entity, detail, entity.start_line))
        except Exception as e:
            logging.error(f"Error during long identifier detection in module {module.name}: {e}", exc_info=True)

        logging.info(
            f"Completed long identifier detection in module: {module.name}. Total smells detected: {len(smells)}")
        return smells
