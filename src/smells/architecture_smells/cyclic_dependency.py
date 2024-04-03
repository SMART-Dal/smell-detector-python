import logging
from collections import defaultdict
from ..smell_detector import ArchitectureSmellDetector
from src.sourcemodel.dependency_graph import DependencyGraph

class CyclicDependencyDetector(ArchitectureSmellDetector):
    def _detect_smells(self, package, config):
        logging.info(f"Starting cyclic dependency detection in package: {package.name}")
        smells = []
        entity = Entity("Cyclic Dependency")

        dependency_graph = DependencyGraph()

        for module in package.modules:
            for sm_class in module.classes:
                dependency_graph.add_module(sm_class.name)
                for external_dependency in sm_class.external_dependencies:
                    dependency_graph.add_dependency(sm_class.name, external_dependency)

        cyclic_dependencies = self._find_cyclic_dependencies(dependency_graph)

        for component1, component2 in cyclic_dependencies:
            detail = f"Cyclic dependency detected between {component1} and {component2}."
            smells.append(self._create_smell(package.name, entity, detail))

        logging.info(
            f"Completed cyclic dependency detection in package: {package.name}. Total smells detected: {len(smells)}"
        )
        return smells

    def _find_cyclic_dependencies(self, dependency_graph):
        cyclic_dependencies = []
        visited = set()

        for component in dependency_graph.graph.nodes:
            if component not in visited:
                stack = [component]
                current_path = set()

                while stack:
                    current_component = stack.pop()
                    current_path.add(current_component)

                    visited.add(current_component)
                    for dependency in dependency_graph.get_dependencies(current_component):
                        if dependency not in visited:
                            stack.append(dependency)
                        else:
                            cyclic_dependencies.append((component, current_component))
                            break

                current_path.remove(current_component)

        return cyclic_dependencies

class Entity:
    def __init__(self, name):
        self.name = name