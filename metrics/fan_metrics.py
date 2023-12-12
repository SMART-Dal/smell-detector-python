def calculate_fan_in_class(py_class):
    return len(py_class.used_classes)


def calculate_fan_out_class(py_class):
    return sum(len(method.called_methods) for method in py_class.methods)


def calculate_fan_in_module(py_module, dependency_graph):
    return dependency_graph.in_degree(py_module.name)


def calculate_fan_out_module(py_module, dependency_graph):
    return dependency_graph.out_degree(py_module.name)
