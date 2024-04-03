import logging

from ..smell_detector import ArchitectureSmellDetector

class AmbiguousInterfaceDetector(ArchitectureSmellDetector):
    def _detect_smells(self, package, config):
        logging.info(f"Starting ambiguous interface detection in package: {package.name}")
        smells = []
        entity = Entity("God Component")
        print(package.modules)

        for module in package.modules:
            if self._check_single_entry_point(module):
                detail = "Single, general entry point detected in the interface, which may lead to ambiguity."
                smells.append(self._create_smell(package.name, entity, detail))

        logging.info(
            f"Completed ambiguous interface detection in package: {package.name}. Total smells detected: {len(smells)}"
        )
        return smells

    def _check_single_entry_point(self, module):
        entry_points = set()
        for entity in self._iterate_functions_and_methods(module):
            if entity.access_modifier == "public":
                entry_points.add(entity.name)
        return len(entry_points) == 1
    
class Entity:
    def __init__(self, name):
        self.name = name