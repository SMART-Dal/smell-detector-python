import networkx as nx


class HierarchyGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_class(self, class_name):
        self.graph.add_node(class_name)

    def add_inheritance(self, child_class, parent_class):
        self.graph.add_edge(parent_class, child_class)

    def analyze_hierarchy(self):
        # Example analysis: Find root classes (classes without parents)
        root_classes = [n for n, d in self.graph.in_degree if d == 0]
        return root_classes

    def display_graph(self):
        # This method can be used to visualize the graph
        nx.draw(self.graph, with_labels=True)
