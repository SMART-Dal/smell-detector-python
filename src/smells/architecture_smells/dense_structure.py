import logging
from collections import defaultdict
from ..smell_detector import ArchitectureSmellDetector
from ..architecture_smells.cyclic_dependency import CyclicDependencyDetector

class DenseStructureDetector(ArchitectureSmellDetector):
    def _detect_smells(self, module, config):
        logging.info(f"Starting Dense Structure detection in module: {module.name}")
        smells = []
        dependency_threshold = 10
        entity = Entity("Dense Structure")

        if self._exceeds_dependency_threshold(module, dependency_threshold):
            if self._has_dense_structure(module):
                detail = "The module has excessive and dense dependencies without a clear structure."
                smells.append(self._create_smell(module.name, entity, detail))

        logging.info(
            f"Completed Dense Structure detection in module: {module.name}. Total smells detected: {len(smells)}"
        )
        return smells

    def _exceeds_dependency_threshold(self, module, dependency_threshold):
        total_dependencies = sum(len(component.dependencies) for component in module.components)
        return total_dependencies > dependency_threshold

    def _has_dense_structure(self, module):
        cyclic_detector = CyclicDependencyDetector()
        cluster = self._cluster_dependencies(module)
        layer = self._layer_dependencies(module)
        cluster_and_layer = cluster and layer
        if cluster_and_layer and not cyclic_detector.detect(module, {}):
            return True
        return False

    def _cluster_dependencies(self, module):
        dependency_clusters = defaultdict(set)
        for component in module.components:
            for dependency in component.dependencies:
                dependency_clusters[dependency].add(component)
        distinct_clusters = len(dependency_clusters)
        cluster_threshold = 5
        return distinct_clusters > cluster_threshold

    def _layer_dependencies(self, module):
        layers = defaultdict(set)
        for component in module.components:
            layers[len(component.dependencies)].add(component)
        return len(layers) > 1
    
class Entity():
     def __init__(self, name):
        self.name = name