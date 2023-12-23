import networkx as nx
import logging


def calculate_lcom4(py_class):
    if not hasattr(py_class, 'methods') or not hasattr(py_class, 'method_interactions'):
        logging.error("Invalid class structure provided to LCOM4 calculation.")
        return 0

    try:
        graph = nx.Graph()
        for method in py_class.methods:
            graph.add_node(method.name)
            for other_method in py_class.methods:
                if method != other_method and py_class.method_interactions.get(method.name).intersection(
                        py_class.method_interactions.get(other_method.name)):
                    graph.add_edge(method.name, other_method.name)

        connected_components = nx.number_connected_components(graph)
        logging.debug(f"LCOM4 calculated: {connected_components}")
        return connected_components
    except Exception as e:
        logging.error(f"Error calculating LCOM4: {e}")
        return 0
