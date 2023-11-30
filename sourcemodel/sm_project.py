from sourcemodel.herrarchy_graph import HierarchyGraph


class PyProject:
    def __init__(self, name):
        self.name = name
        self.modules = []
        self.hierarchy_graph = HierarchyGraph()
        # self.dependency_graph = DependencyGraph()

    def add_module(self, module):
        self.modules.append(module)

    def analyze_project(self):
        for module in self.modules:
            module.analyze()




