import logging

from ..smell_detector import ArchitectureSmellDetector

class AmbiguousInterfaceDetector(ArchitectureSmellDetector):
    def _detect_smells(self, package_details, config):
        for package_name, modules in package_details.items():
            logging.info(f"Starting ambiguous interface detection in package: {package_name}")
            package_smells = self._detect_ambiguous_interface_smells(modules, config, package_name)
            logging.info(
                f"Completed ambiguous interface detection in package: {package_name}. Total smells detected: {len(package_smells)}"
            )

        return package_smells

    def _detect_ambiguous_interface_smells(self, modules, config, package_name):
        smells = []
        entity = Entity("God Component")
        for module in modules:
            for entity in self._iterate_functions_and_methods(module):
                if self._check_single_entry_point(entity):
                    detail = "Single, general entry point detected in the interface, which may lead to ambiguity."
                    smells.append(self._create_smell(package_name, entity, detail))

        return smells if len(smells)==1 else []

    def _check_single_entry_point(self, entity):
        if hasattr(entity, 'access_modifier') and entity.access_modifier == "public":
            return True
        return False
    
class Entity:
    def __init__(self, name):
        self.name = name