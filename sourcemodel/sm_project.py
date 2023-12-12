from sourcemodel.dependency_graph import DependencyGraph
from sourcemodel.hierarchy_graph import HierarchyGraph


class PyProject:
    def __init__(self, name):
        self.name = name
        self.modules = []
        self.packages = []
        self.hierarchy_graph = HierarchyGraph()
        self.dependency_graph = DependencyGraph()

    def add_module(self, module):
        module.dependency_graph = self.dependency_graph
        self.modules.append(module)

    def add_package(self, package):
        self.packages.append(package)

    def analyze_project(self):
        for module in self.modules:
            module.analyze()
