import logging

from ..smell_detector import ArchitectureSmellDetector

class AmbiguousInterfaceDetector(ArchitectureSmellDetector):
    def _detect_smells(self, module, config):
        logging.info(f"Starting ambiguous interface detection in module: {module.name}")
        smells = []

        if self._check_single_entry_point(module):
            detail = "Single, general entry point detected in the interface, which may lead to ambiguity."
            smells.append(self._create_smell(module.name, "Ambiguous Interface", detail))

        logging.info(
            f"Completed ambiguous interface detection in module: {module.name}. Total smells detected: {len(smells)}"
        )
        return smells

    def _check_single_entry_point(self, module):
        entry_points = set()
        for entity in self._iterate_functions_and_methods(module):
            if entity.access_modifier == "public":  # Assuming public methods are entry points
                entry_points.add(entity.name)
        print(len(entry_points))
        return len(entry_points) == 1