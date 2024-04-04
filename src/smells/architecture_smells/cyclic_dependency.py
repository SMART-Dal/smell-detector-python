import logging
from collections import defaultdict
from ..smell_detector import ArchitectureSmellDetector
from src.sourcemodel.dependency_graph import DependencyGraph

class CyclicDependencyDetector(ArchitectureSmellDetector):
    def _detect_smells(self, package_details, config):
        logging.info("I am here")
        all_smells = []
        
        dependency_graph = DependencyGraph()
        module_to_package_mapping = {}
        for package_name, modules in package_details.items():
            for module in modules:
                module_to_package_mapping[module] = package_name

        for package_name, modules in package_details.items():
            for module in modules:
                dependency_graph.add_module(module.name)
                for sm_class in module.classes:
                    for external_dependency in sm_class.external_dependencies:
                        dependency_graph.add_dependency(module.name, external_dependency)
                        
        dependent_lst = {}
        for package_name, modules in package_details.items():
            for module in modules:
                dependecies = dependency_graph.get_dependencies(module)
                for dependency in dependecies:
                    parent_package_name = module_to_package_mapping[dependency]
                    if parent_package_name not in dependent_lst:
                        dependent_lst[parent_package_name] = set()
                    dependent_lst[parent_package_name].add(package_name)
                    

        cycles = self.find_cycles(dependent_lst)
        package_smells = []
        
        for cycle in cycles:
            for components in cycle:
                detail = f"{components} detected in a Cycle!"
                entity = Entity("Cyclic Dependency")
                package_smells.append(self._create_smell(package_name, entity, detail))
                all_smells.extend(package_smells)
        logging.info(
                f"Completed cyclic dependency detection."
            )

        return all_smells
        

    def find_cycles(self, graph):
        def dfs(node, parent, path):
            visited.add(node)
            path.append(node)
            for neighbor in graph[node]:
                if neighbor not in visited:
                    dfs(neighbor, node, path)
                elif neighbor != parent:
                    cycle = path[path.index(neighbor):] + [neighbor]
                    cycles.append(cycle)
            path.pop()

        visited = set()
        cycles = []
        for node in graph:
            if node not in visited:
                dfs(node, None, [])
        return cycles

class Entity:
    def __init__(self, name):
        self.name = name