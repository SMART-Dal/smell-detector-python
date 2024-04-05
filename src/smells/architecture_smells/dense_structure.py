import logging
from ..smell_detector import ArchitectureSmellDetector
from src.sourcemodel.dependency_graph import DependencyGraph

class DenseStructureDetector(ArchitectureSmellDetector):
    def _detect_smells(self, package_details, config):
        logging.info(
            f"Starting Dense Structure Smell Detection."
        )
        all_smells = []
        threshold = 5
        
        dependency_graph = self._build_dependency_graph(package_details)
        average_degree = self._compute_average_degree(dependency_graph)
        
        if average_degree > threshold:
            entity = Entity("Dense Structure")
            detail = f"The average degree of the dependency graph is {average_degree}, which exceeds the threshold of {threshold}."
            all_smells.append(self._create_smell("Repository", entity, detail))
        
        logging.info(
            f"Completed Dense Structure detection. Total smells detected: {len(all_smells)}"
        )
        return all_smells
    
    def _build_dependency_graph(self, package_details):
        dependency_graph = DependencyGraph()
        
        for package_name, modules in package_details.items():
            for module in modules:
                for sm_class in module.classes:
                    dependency_graph.add_module(sm_class.name)
                    for dependency in sm_class.external_dependencies:
                        dependency_graph.add_dependency(sm_class.name, dependency)
        
        return dependency_graph
    
    def _compute_average_degree(self, dependency_graph):
        num_edges = dependency_graph.graph.number_of_edges()
        num_vertices = dependency_graph.graph.number_of_nodes()
        if num_vertices == 0:
            return 0
        return 2 * num_edges / num_vertices

class Entity:
    def __init__(self, name):
        self.name = name