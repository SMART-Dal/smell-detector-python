import logging

import networkx as nx


# import matplotlib.pyplot as plt


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

    def get_ancestors(self, class_name):
        ancestors = set()
        to_visit = [class_name]
        while to_visit:
            current_class = to_visit.pop()
            parents = list(self.graph.predecessors(current_class))
            ancestors.update(parents)
            to_visit.extend(parents)
        return ancestors

    def has_multipath_inheritance(self, class_name):
        try:
            ancestors = self.get_ancestors(class_name)
            for ancestor in ancestors:
                paths = list(nx.all_simple_paths(self.graph, ancestor, class_name))
                if len(paths) > 1:
                    logging.debug(f"Multipath inheritance detected for {class_name} from {ancestor}")
                    return True, ancestor
            return False, None
        except Exception as e:
            logging.error(f"Error checking multipath inheritance for {class_name}: {e}")
            return False, None

    # def visualize_graph(self):
    #     pos = nx.circular_layout(self.graph)  # Use circular layout for better spacing
    #     plt.figure(figsize=(8, 8))  # Adjust figure size
    #     nx.draw(self.graph, pos, with_labels=True, node_size=500, node_color='lightblue')
    #     plt.title("Hierarchy Graph")
    #     plt.show()
