# import logging

# from ..smell_detector import ArchitectureSmellDetector
# from src.sourcemodel.dependency_graph import DependencyGraph

# class UnstableDependencyDetector(ArchitectureSmellDetector):
#     def _detect_smells(self, module, config):
#         logging.info(f"Starting Unstable Dependency detection in module: {module.name}")
#         smells = []
#         entity = Entity("Unstable Dependency")
#         dependency_graph = DependencyGraph()

#         # Analyze each component in the module
#         for component in module.classes + module.functions:
#             print(component)
#             # Calculate the stability of the component
#             stability = self._calculate_stability(component,dependency_graph)

#             # If the stability is less than a certain threshold, it indicates an unstable dependency
#             if stability < config.get("stability_threshold", 0.5):
#                 detail = f"The component '{component.name}' has unstable dependencies."
#                 smells.append(self._create_smell(module.name, entity, detail))

#         logging.info(
#             f"Completed Unstable Dependency detection in module: {module.name}. Total smells detected: {len(smells)}"
#         )
#         return smells

#     def _calculate_stability(self, component, dependency_graph):
#         """
#         Calculate the stability of a component.
#         Stability = outgoing dependencies / (incoming dependencies + outgoing dependencies)
#         """
#         outgoing_dependencies = len(dependency_graph.get_dependencies(component))
#         print(outgoing_dependencies)
#         if outgoing_dependencies == 0:
#             return 0.0

#         # Get all modules that depend on the given component
#         incoming_dependencies = sum(1 for module in dependency_graph.graph.nodes() if component in dependency_graph.get_dependencies(module))

#         return outgoing_dependencies / (incoming_dependencies + outgoing_dependencies)
    
# class Entity():
#     def __init__(self, name):
#         self.name = name