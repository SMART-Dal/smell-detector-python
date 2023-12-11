def calculate_nof(py_class):
    return len(py_class.fields)


def calculate_nopf(py_class):
    return sum(1 for field, access in py_class.fields.items() if access == 'public')


def calculate_module_nof(py_module):
    return len(py_module.global_variables)


def calculate_module_nopf(py_module):
    return sum(1 for var in py_module.global_variables if not var.startswith('_'))
