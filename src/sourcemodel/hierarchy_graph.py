import networkx as nx


class HierarchyGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_class(self, class_name):
        self.graph.add_node(class_name)

    def add_inheritance(self, child_class, parent_class):
        self.graph.add_edge(parent_class, child_class)

