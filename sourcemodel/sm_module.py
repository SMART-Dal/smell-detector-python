from metrics.method_metrics import calculate_class_loc, calculate_cyclomatic_complexity, calculate_function_loc, \
    calculate_parameter_count, calculate_module_loc


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
        param_count = calculate_parameter_count(py_method)

        return {
            'package': self.package_name,
            'module_name': self.name,
            'class_name': class_name,
            'method_name': py_method.name,
            'loc': calculate_function_loc(py_method),
            'cc': complexity,
            'pc': param_count
        }

    def analyze_function(self, py_function):
        complexity = calculate_cyclomatic_complexity(py_function.ast_node)
        param_count = calculate_parameter_count(py_function)

        return {
            'package': self.package_name,
            'module_name': self.name,
            'function_name': py_function.name,
            'loc': calculate_function_loc(py_function),
            'cc': complexity,
            'pc': param_count
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
            # print(f"Analyzing class: {py_class.name}")
            for method in py_class.methods:
                # print(f"Analyzing method: {method.name}")
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
