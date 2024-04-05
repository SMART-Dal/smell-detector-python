import logging
from ..smell_detector import ArchitectureSmellDetector
from src.sourcemodel.dependency_graph import DependencyGraph

class UnstableDependencyDetector(ArchitectureSmellDetector):
    def _detect_smells(self, package_details, config):
        logging.info(
            f"Starting Unstable Dependency detection."
        )
        all_smells = []
        
        module_to_package_mapping = {}
        for package_name, modules in package_details.items():
            for module in modules:
                module_to_package_mapping[module.name] = package_name
                        
        dependent_lst = {}
        for package_name, modules in package_details.items():
            for module in modules:
                dependencies = module.dependency_graph.get_dependencies(module.name)
                for dependency in dependencies:
                    parent_package_name = module_to_package_mapping.get(dependency)

                    # Skip external dependency or dependency within the same package
                    if parent_package_name is None or package_name == parent_package_name:
                        continue
                    
                    if parent_package_name not in dependent_lst:
                        dependent_lst[parent_package_name] = set()
                    dependent_lst[parent_package_name].add(package_name)
        
        
        for package_name, dependencies in dependent_lst.items():
            incoming_dependencies = len(dependencies)
            outgoing_dependencies = sum(1 for dep in dependent_lst.values() if package_name in dep)

            instability = outgoing_dependencies / (outgoing_dependencies + incoming_dependencies)
            instability_threshold = config.get('instability_threshold', 0.5)

            if instability > instability_threshold:
                entity = Entity("Unstable Dependency")
                detail = f"{package_name} has instability {instability}, which exceeds the threshold of {instability_threshold}."
                all_smells.append(self._create_smell(package_name, entity, detail))

        
        logging.info(
            f"Completed Unstable Dependency detection. Total smells detected: {len(all_smells)}"
        )
        return all_smells

class Entity:
    def __init__(self, name):
        self.name = name