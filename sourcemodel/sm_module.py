from metrics.cyclomatic_complexity import calculate_cyclomatic_complexity
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
            'module_name': self.name,
            'class_name': py_class.name,
            'loc': calculate_class_loc(py_class)
        }

    def analyze_methods(self, py_method, class_name):
        complexity = calculate_cyclomatic_complexity(py_method.ast_node)
        return {
            'package': self.package_name,
            'module_name': self.name,
            'class_name': class_name,
            'method_name': py_method.name,
            'loc': calculate_function_loc(py_method),
            'cc': complexity
        }

    def analyze_function(self, py_function):
        complexity = calculate_cyclomatic_complexity(py_function.ast_node)
        return {
            'package': self.package_name,
            'module_name': self.name,
            'function_name': py_function.name,
            'loc': calculate_function_loc(py_function),
            'cc': complexity
        }

    def analyze(self):
        module_metrics = {
            'package': self.package_name,
            'module_name': self.name,
            'loc': calculate_module_loc(self)
        }

        # Aggregate metrics for each class in the module
        class_metrics = [self.analyze_class(py_class) for py_class in self.classes]

        method_metrics = []
        function_metrics = []
        for py_class in self.classes:

            for method in py_class.methods:
                analyzed_method = self.analyze_methods(method, py_class.name)
                method_metrics.append(analyzed_method)

        for function in self.functions:
            analyzed_function = self.analyze_function(function)
            function_metrics.append(analyzed_function)

        return {
            'module_metrics': module_metrics,
            'class_metrics': class_metrics,
            'method_metrics': method_metrics,
            'function_metrics': function_metrics,
        }
