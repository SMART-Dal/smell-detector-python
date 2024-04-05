import logging
from ..smell_detector import ArchitectureSmellDetector

class ScatteredFunctionalityDetector(ArchitectureSmellDetector):
    def _detect_smells(self, package_details, config):
        logging.info(
            f"Starting Scattered Functionality detection."
        )
        all_smells = []

        for package_name, modules in package_details.items():
            for module in modules:
                for sm_class in module.classes:
                    for method in sm_class.methods:
                        accessed_components = self._get_accessed_components(method, package_name)
                        print(len(accessed_components))
                        if len(accessed_components) > 1:
                            entity = Entity("Scattered Functionality")
                            detail = f"Method {method.name} in class {sm_class.name} accesses multiple components: {', '.join(accessed_components)}"
                            all_smells.append(self._create_smell(package_name, entity, detail))

        logging.info(
            f"Completed Scattered Functionality detection. Total smells detected: {len(all_smells)}"
        )
        return all_smells

    def _get_accessed_components(self, method, package_name):
        accessed_components = set()
        method_package = package_name
        for module in method.used_modules:
            component = self._get_component_from_identifier(module)
            if component and component != method_package:
                accessed_components.add(component)
        return accessed_components

    def _get_component_from_identifier(self, identifier):
        components = identifier.split('.')
        if len(components) > 2:
            return components[1]
        return None

class Entity:
    def __init__(self, name):
        self.name = name
