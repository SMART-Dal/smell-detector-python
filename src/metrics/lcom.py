import networkx as nx


def calculate_lcom4(py_class):
    # Create a graph for the class
    try:
        graph = nx.Graph()

        # Debugging: Check if method interactions are populated
        # print(f"Method interactions for class {py_class.name}: {py_class.method_interactions}")

        # Add nodes (methods) to the graph
        for method in py_class.methods:
            graph.add_node(method.name)
            # print(f"Added node for method: {method.name}")

        # Add edges based on shared field access
        for method_name, accessed_fields in py_class.method_interactions.items():
            for other_method in py_class.methods:
                if method_name != other_method.name and accessed_fields.intersection(
                        py_class.method_interactions[other_method.name]):
                    graph.add_edge(method_name, other_method.name)
                    # print(f"Added edge between {method_name} and {other_method.name}")

        # Check if graph is empty
        if graph.number_of_nodes() == 0:
            # print("Graph is empty. No methods or shared field accesses.")
            return 0

        # print("Calculating number of connected components...")
        # Calculate the number of connected components
        connected_components = nx.number_connected_components(graph)
        # print(f"Number of connected components (LCOM4): {connected_components}")

        return connected_components

    except Exception as e:
        print(f"Exception occurred: {e}")

# import networkx as nx
#
#
# def calculate_lcom4(py_class):
#     graph = nx.Graph()
#
#     # Add methods and fields as nodes
#     for method in py_class.methods:
#         graph.add_node(method.name)
#         for field in method.called_methods:
#             graph.add_node(field)
#             graph.add_edge(method.name, field)
#
#     # Add fields that are not accessed by any method
#     for field in py_class.class_fields:
#         if field not in graph:
#             graph.add_node(field)
#
#     # Calculate the number of connected components
#     connected_components = nx.number_connected_components(graph)
#
#     # LCOM4 is the number of connected components minus one
#     lcom4 = max(0, connected_components - 1)
#     return lcom4
