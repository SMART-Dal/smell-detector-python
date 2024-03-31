import networkx as nx


class DependencyGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_module(self, module_name):
        self.graph.add_node(module_name)

    def add_dependency(self, from_module, to_module_full):
        to_module = to_module_full.split('.')[0] + '.py'  # Extracting just the module name
        # print(f"from_module: {from_module}, to_module: {to_module}")
        self.graph.add_edge(from_module, to_module)
        
    def get_dependencies(self, component):
        dependencies = []
        for from_module, to_module in self.graph.edges():
            if from_module == component:
                dependencies.append(to_module)
        return dependencies