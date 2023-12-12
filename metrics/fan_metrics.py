def calculate_fan_in_class(py_class):
    print(f"Fan in: Method interactions {py_class.name} : {py_class.method_interactions}")
    return len(py_class.method_interactions)


def calculate_fan_out_class(py_class):
    print(f"Fab out: External dep {py_class.name} : {py_class.external_dependencies}")
    return len(py_class.external_dependencies)


def calculate_fan_in_module(py_module, dependency_graph):
    # print(f"In Edges {py_module.name}: {dependency_graph.in_edges(py_module.name)}")
    return dependency_graph.in_degree(py_module.name)


def calculate_fan_out_module(py_module, dependency_graph):
    # print(f"Out Edges {py_module.name}: {dependency_graph.out_edges(py_module.name)}")
    return dependency_graph.out_degree(py_module.name)
