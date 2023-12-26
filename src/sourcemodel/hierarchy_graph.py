import networkx as nx


class HierarchyGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_class(self, class_name):
        self.graph.add_node(class_name)

    def add_inheritance(self, child_class, parent_class):
        self.graph.add_edge(parent_class, child_class)

    def get_inheritance_depth(self, class_name):
        if class_name not in self.graph:
            return 0  # Class not found in the graph
        depth = 0
        while list(self.graph.predecessors(class_name)):
            depth += 1
            class_name = next(self.graph.predecessors(class_name))
        return depth
