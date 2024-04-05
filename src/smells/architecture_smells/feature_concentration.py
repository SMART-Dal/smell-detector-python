import logging
from ..smell_detector import ArchitectureSmellDetector
from src.sourcemodel.dependency_graph import DependencyGraph

class FeatureConcentrationDetector(ArchitectureSmellDetector):
    def _detect_smells(self, package_details, config):
        all_smells = []

        lcc_threshold = 0.2

        for package_name, modules in package_details.items():
            smells=[]
            logging.info(f"Starting Feature Concentration detection in package: {package_name}")
            entity = Entity("Feature Concentration")
            total_num_classes = 0
            total_disconnected_subgraphs = 0

            for module in modules:
                dependency_graph = self._build_dependency_graph(module)
                num_classes = len(module.classes)
                total_num_classes += num_classes

                disconnected_subgraphs = self._count_disconnected_subgraphs(dependency_graph)
                total_disconnected_subgraphs += disconnected_subgraphs

            if total_num_classes > 0 and total_disconnected_subgraphs > 1:
                lcc = total_disconnected_subgraphs / total_num_classes
                if lcc > lcc_threshold:
                    detail = f"The package {package_name} has Lack of Component Cohesion (LCC) of {lcc}, which exceeds the threshold of {lcc_threshold}."
                    smells.append(self._create_smell(package_name, entity, detail))
            all_smells.extend(smells)

            logging.info(
                f"Completed Feature Concentration detection in package: {package_name}. Total smells detected: {len(all_smells)}"
            )

        return all_smells
    
    def _build_dependency_graph(self, module):
        dependency_graph = DependencyGraph()
        
        for sm_class in module.classes:
            dependency_graph.add_module(sm_class.name)
            for dependency in sm_class.external_dependencies:
                dependency_graph.add_dependency(sm_class.name, dependency)
        
        return dependency_graph
    
    def _count_disconnected_subgraphs(self, dependency_graph):
        return len(list(dependency_graph.weakly_connected_components()))

class Entity:
    def __init__(self, name):
        self.name = name