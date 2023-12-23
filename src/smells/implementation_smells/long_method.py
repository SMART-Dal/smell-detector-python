import logging

from ..smell_detector import ImplementationSmellDetector


class LongMethodDetector(ImplementationSmellDetector):
    def _detect_smells(self, module, config):
        logging.debug(f"Starting long method detection in {module.name}")
        smells = []
        max_lines = config.get("threshold", 20)  # Default to 20 if not specified

        for entity in self._iterate_functions_and_methods(module):
            try:
                if entity.loc > max_lines:
                    detail = f"Method '{entity.name}' is too long ({entity.loc} lines)."
                    location = f"{entity.start_line} - {entity.end_line}"
                    smells.append(self._create_smell(module.name, entity, detail, location))
                    logging.info(f"Long method detected: {entity.name} ({entity.loc} lines) in {module.name}")
            except Exception as e:
                logging.error(f"Error analyzing {entity.name} in {module.name}: {e}", exc_info=True)

        logging.info(
            f"Completed long method detection in module: {module.name}. Total smells detected: {len(smells)}")
        return smells
