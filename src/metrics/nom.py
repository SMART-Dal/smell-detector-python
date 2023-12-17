def calculate_nom(py_class):
    return len(py_class.methods)


def calculate_nopm(py_class):
    return sum(1 for method in py_class.methods if not method.name.startswith('_'))
