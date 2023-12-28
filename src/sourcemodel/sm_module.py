from src import metrics
from src.metrics import calculate_function_loc, calculate_cyclomatic_complexity, calculate_parameter_count
from src.sourcemodel.dependency_graph import DependencyGraph


class SMModule:
    def __init__(self, name, project=None, package_name=None, input_dependency_graph=None):
        self.name = name
        self.project = project
        self.package_name = package_name
        self.dependency_graph: DependencyGraph = input_dependency_graph
        self.classes = []
        self.functions = []
        self.imports = []
        self.global_variables = []

    def add_class(self, sm_class):
        self.classes.append(sm_class)

    def add_function(self, sm_function):
        self.functions.append(sm_function)
        for module_name in sm_function.used_modules:
            self.dependency_graph.add_dependency(self.name, module_name)

    def add_import(self, sm_import):
        self.imports.append(sm_import)

    def add_global_variable(self, variable_name):
        if variable_name not in self.global_variables:
            self.global_variables.append(variable_name)

    def analyze(self):

        module_metrics = self.calculate_module_metrics()
        class_metrics = [self.analyze_class(sm_class) for sm_class in self.classes]
        method_metrics = [self.analyze_method_or_function(method, sm_class.name)
                          for sm_class in self.classes for method in sm_class.methods]
        function_metrics = [self.analyze_method_or_function(function) for function in self.functions]

        return {
            'module_metrics': module_metrics,
            'class_metrics': class_metrics,
            'method_metrics': method_metrics,
            'function_metrics': function_metrics,
        }

    def calculate_module_metrics(self):
        dependency_graph = self.dependency_graph.graph

        module_nom = sum(metrics.calculate_nom(sm_class) for sm_class in self.classes)
        module_nopm = sum(metrics.calculate_nopm(sm_class) for sm_class in self.classes) + len(self.functions)

        return {
            'package': self.package_name,
            'module_name': self.name,
            'loc': metrics.calculate_module_loc(self),
            'wmc': metrics.calculate_wmc_for_module(self),
            'nom': module_nom,
            'nopm': module_nopm,
            'nof': metrics.calculate_module_nof(self),
            'nopf': metrics.calculate_module_nopf(self),
            'fan_in': metrics.calculate_fan_in_module(self, dependency_graph),
            'fan_out': metrics.calculate_fan_out_module(self, dependency_graph)
        }

    def analyze_class(self, sm_class):
        metrics_dict = {
            'package': self.package_name,
            'module_name': self.name,
            'class_name': sm_class.name,
            'loc': metrics.calculate_class_loc(sm_class),
            'wmc': metrics.calculate_wmc_for_class(sm_class),
            'nom': metrics.calculate_nom(sm_class),
            'nopm': metrics.calculate_nopm(sm_class),
            'nof': metrics.calculate_nof(sm_class),
            'nopf': metrics.calculate_nopf(sm_class),
            'lcom': metrics.calculate_lcom4(sm_class),
            'fan_in': metrics.calculate_fan_in_class(sm_class),
            'fan_out': metrics.calculate_fan_out_class(sm_class)
        }

        sm_class.set_metrics(metrics_dict)

        return metrics_dict

    def analyze_method_or_function(self, item, class_name=None):
        lines = calculate_function_loc(item)
        complexity = calculate_cyclomatic_complexity(item.ast_node)
        param_count = calculate_parameter_count(item)

        item.set_metrics(lines, complexity, param_count)

        function_method_metrics = {
            'package': self.package_name,
            'module_name': self.name,
            'loc': lines,
            'cc': complexity,
            'pc': param_count
        }
        if class_name:
            function_method_metrics['class_name'] = class_name
            function_method_metrics['method_name'] = item.name
        else:
            function_method_metrics['function_name'] = item.name
        return function_method_metrics
