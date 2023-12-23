import logging

from ..smell_detector import ImplementationSmellDetector


class LongParameterListDetector(ImplementationSmellDetector):
    def _detect_smells(self, module, config):
        logging.info(f"Starting long parameter list detection in module: {module.name}")
        smells = []
        max_params = config.get("threshold", 5)  # Default to 5 if not specified

        for entity in self._iterate_functions_and_methods(module):
            try:
                if entity.parameter_count > max_params:
                    detail = f"{entity.name} has {entity.parameter_count} parameters, exceeding the max of {max_params}."
                    location = f"{entity.start_line} - {entity.end_line}"
                    smells.append(self._create_smell(module.name, entity, detail, location))
                    logging.info(
                        f"Long parameter list detected in {entity.name} ({entity.parameter_count} parameters) at lines {location} in {module.name}")
            except Exception as e:
                logging.error(f"Error analyzing {entity.name} in {module.name}: {e}", exc_info=True)

        logging.info(
            f"Completed long parameter list detection in module: {module.name}. Total smells detected: {len(smells)}")
        return smells
