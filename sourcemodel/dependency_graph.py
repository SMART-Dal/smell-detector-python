import networkx as nx


class DependencyGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_module(self, module_name):
        self.graph.add_node(module_name)

    def add_dependency(self, from_module, to_module):
        self.graph.add_edge(from_module, to_module)

    def analyze_dependencies(self):
        # Example analysis: Identify modules with the most dependencies
        most_dependent_modules = sorted(self.graph.out_degree, key=lambda x: x[1], reverse=True)
        return most_dependent_modules

    def display_graph(self):
        # This method can be used to visualize the graph
        nx.draw(self.graph, with_labels=True)
