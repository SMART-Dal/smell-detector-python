def calculate_fan_in_class(py_class):
    return 0


def calculate_fan_out_class(py_class):
    return 0


def calculate_fan_in_module(py_module, dependency_graph):
    # print(f"In Edges {py_module.name}: {dependency_graph.in_edges(py_module.name)}")
    return dependency_graph.in_degree(py_module.name)


def calculate_fan_out_module(py_module, dependency_graph):
    # print(f"Out Edges {py_module.name}: {dependency_graph.out_edges(py_module.name)}")
    return dependency_graph.out_degree(py_module.name)
