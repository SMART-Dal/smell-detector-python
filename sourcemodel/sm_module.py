from metrics.cc import calculate_cyclomatic_complexity
from metrics.fan_metrics import calculate_fan_in_class, calculate_fan_out_class, calculate_fan_in_module, \
    calculate_fan_out_module
from metrics.lcom import calculate_lcom4
from metrics.loc import calculate_class_loc, calculate_function_loc, calculate_module_loc
from metrics.nof import calculate_nof, calculate_nopf, calculate_module_nof, calculate_module_nopf
from metrics.nom import calculate_nom, calculate_nopm
from metrics.pc import calculate_parameter_count
from metrics.wmc import calculate_wmc_for_class, calculate_wmc_for_module
from sourcemodel.dependency_graph import DependencyGraph


class PyModule:
    def __init__(self, name, package_name=None, input_dependency_graph=None):
        self.name = name
        self.package_name = package_name
        self.dependency_graph: DependencyGraph = input_dependency_graph
        self.classes = []
        self.functions = []
        self.imports = []
        self.global_variables = []

    def add_class(self, py_class):
        self.classes.append(py_class)

    def add_function(self, py_function):
        self.functions.append(py_function)
        for module_name in py_function.used_modules:
            self.dependency_graph.add_dependency(self.name, module_name)

    def add_import(self, py_import):
        self.imports.append(py_import)

    def add_global_variable(self, variable_name):
        if variable_name not in self.global_variables:
            self.global_variables.append(variable_name)

    def analyze(self):

        module_metrics = self.calculate_module_metrics()
        class_metrics = [self.analyze_class(py_class) for py_class in self.classes]
        method_metrics = [self.analyze_method_or_function(method, py_class.name)
                          for py_class in self.classes for method in py_class.methods]
        function_metrics = [self.analyze_method_or_function(function) for function in self.functions]

        return {
            'module_metrics': module_metrics,
            'class_metrics': class_metrics,
            'method_metrics': method_metrics,
            'function_metrics': function_metrics,
        }

    def calculate_module_metrics(self):
        dependency_graph = self.dependency_graph.graph

        module_nom = sum(calculate_nom(py_class) for py_class in self.classes)
        module_nopm = sum(calculate_nopm(py_class) for py_class in self.classes) + len(self.functions)

        return {
            'package': self.package_name,
            'module_name': self.name,
            'loc': calculate_module_loc(self),
            'wmc': calculate_wmc_for_module(self),
            'nom': module_nom,
            'nopm': module_nopm,
            'nof': calculate_module_nof(self),
            'nopf': calculate_module_nopf(self),
            'fan_in': calculate_fan_in_module(self, dependency_graph),
            'fan_out': calculate_fan_out_module(self, dependency_graph)
        }

    def analyze_class(self, py_class):
        # print(f"analyzing {self.name} : {py_class.name}")
        return {
            'package': self.package_name,
            'module_name': self.name,
            'class_name': py_class.name,
            'loc': calculate_class_loc(py_class),
            'wmc': calculate_wmc_for_class(py_class),
            'nom': calculate_nom(py_class),
            'nopm': calculate_nopm(py_class),
            'nof': calculate_nof(py_class),
            'nopf': calculate_nopf(py_class),
            'lcom': calculate_lcom4(py_class),
            'fan_in': calculate_fan_in_class(py_class),
            'fan_out': calculate_fan_out_class(py_class)
        }

    def analyze_method_or_function(self, item, class_name=None):
        lines = calculate_function_loc(item)
        complexity = calculate_cyclomatic_complexity(item.ast_node)
        param_count = calculate_parameter_count(item)

        item.set_metrics(lines, complexity, param_count)

        metrics = {
            'package': self.package_name,
            'module_name': self.name,
            'loc': lines,
            'cc': complexity,
            'pc': param_count
        }
        if class_name:
            metrics['class_name'] = class_name
            metrics['method_name'] = item.name
        else:
            metrics['function_name'] = item.name
        return metrics
