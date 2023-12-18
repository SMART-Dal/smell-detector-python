from src.sourcemodel.dependency_graph import DependencyGraph
from src.sourcemodel.hierarchy_graph import HierarchyGraph


class SMProject:
    def __init__(self, name):
        self.name = name
        self.modules = []
        self.packages = []
        self.hierarchy_graph = HierarchyGraph()
        self.dependency_graph = DependencyGraph()

    def add_module(self, module):
        # print(f"Adding module: {module.name}")
        module.dependency_graph = self.dependency_graph
        self.modules.append(module)

    def add_package(self, package):
        self.packages.append(package)

    def analyze_project(self):
        for module in self.modules:
            module.analyze()

    def find_class(self, class_name):
        for module in self.modules:
            for py_class in module.classes:
                if py_class.name == class_name:
                    return py_class
        return None
