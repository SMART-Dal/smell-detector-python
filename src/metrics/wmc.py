from metrics.cc import calculate_cyclomatic_complexity


def calculate_wmc_for_class(py_class):
    return sum(calculate_cyclomatic_complexity(method.ast_node) for method in py_class.methods)


def calculate_wmc_for_module(py_module):
    return sum(calculate_wmc_for_class(py_class) for py_class in py_module.classes)
