from metrics.loc_calculator import calculate_module_loc, calculate_class_loc, calculate_function_loc


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

    def analyze_class(self, py_class):
        return {
            'package': self.package_name,
            'class_name': py_class.name,
            'loc': calculate_class_loc(py_class)
        }

    def analyze_methods(self, py_method, class_name):
        return {
            'package': self.package_name,
            'class_name': class_name,
            'method_name': py_method.name,
            'loc': calculate_function_loc(py_method)
        }

    def analyze_function(self, py_function):
        return {
            'package': self.package_name,
            'function_name': py_function.name,
            'loc': calculate_function_loc(py_function)
        }

    def analyze(self):
        # Initialize data structures for analysis results
        module_metrics = {
            'package': self.package_name,
            'module_name': self.name,
            'loc': calculate_module_loc(self)
        }

        # Aggregate metrics for each class in the module
        class_metrics = [self.analyze_class(py_class) for py_class in self.classes]
        method_metrics = []

        for py_class in self.classes:
            for method in py_class.methods:
                method_metrics.append(self.analyze_methods(method, py_class.name))

        # Aggregate metrics for each function in the module
        # Note: Standalone functions
        function_metrics = [self.analyze_function(py_function) for py_function in self.functions]

        return {
            'module_metrics': module_metrics,
            'class_metrics': class_metrics,
            'method_metrics': method_metrics,
            'function_metrics': function_metrics,
        }
