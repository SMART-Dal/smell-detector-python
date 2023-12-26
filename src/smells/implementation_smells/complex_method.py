import logging

from ..smell_detector import ImplementationSmellDetector


class ComplexMethodDetector(ImplementationSmellDetector):
    def _detect_smells(self, module, config):
        smells = []
        max_complexity = config.get("threshold", 10)  # Default to 10 if not specified

        for entity in self._iterate_functions_and_methods(module):
            try:
                # Check the complexity of each entity (function or method)
                if hasattr(entity, 'complexity') and entity.complexity > max_complexity:
                    detail = f"Method '{entity.name}' has a cyclomatic complexity of {entity.complexity}, exceeding the max of {max_complexity}."
                    location = f"{entity.start_line} - {entity.end_line}"
                    smells.append(self._create_smell(module.name, entity, detail, location))
            except Exception as e:
                logging.error(f"Error analyzing complexity for {entity.name} in {module.name}: {e}", exc_info=True)

        logging.info(
            f"Completed complex method detection in module: {module.name}. Total smells detected: {len(smells)}")
        return smells
