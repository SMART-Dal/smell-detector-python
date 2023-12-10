from metrics.loc_calculator import calculate_module_loc, calculate_class_loc, calculate_function_loc


def analyze_class(py_class):
    return {
        'name': py_class.name,
        'loc': calculate_class_loc(py_class)
    }


def analyze_methods(py_methods):
    return {
        'name': py_methods.name,
        'loc': calculate_class_loc(py_methods)
    }


def analyze_function(py_function):
    return {
        'name': py_function.name,
        'loc': calculate_function_loc(py_function)
    }


class PyModule:
    def __init__(self, name, package_name=None):
        self.name = name
        self.package_name = package_name
        self.classes = []
        self.functions = []
        self.imports = []

    def add_class(self, py_class):
        self.classes.append(py_class)

    def add_function(self, py_function):
        self.functions.append(py_function)

    def add_import(self, py_import):
        self.imports.append(py_import)

    def analyze(self):
        # Initialize data structures for analysis results
        module_metrics = {
            'package': self.package_name,
            'name': self.name,
            'loc': calculate_module_loc(self)
        }

        # Aggregate metrics for each class in the module
        class_metrics = [analyze_class(py_class) for py_class in self.classes]

        # Aggregate metrics for each function in the module
        # Note: Standalone functions
        method_metrics = [analyze_function(py_function) for py_function in self.functions]

        return {
            'module_metrics': module_metrics,
            'class_metrics': class_metrics,
            'method_metrics': method_metrics,
        }
