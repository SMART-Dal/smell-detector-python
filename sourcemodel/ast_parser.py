import ast
import os

from sourcemodel.ast_utils import get_return_type, get_function_body_and_variables, determine_access_modifier, \
    get_decorators, get_annotation, extract_package_name
from sourcemodel.sm_class import PyClass
from sourcemodel.sm_function import PyFunction
from sourcemodel.sm_import import PyImport
from sourcemodel.sm_method import PyMethod
from sourcemodel.sm_module import PyModule
from sourcemodel.sm_parameter import PyParameter


def populate_function_details(py_function, return_type, function_body, local_variables):
    py_function.set_return_type(return_type)
    for statement in function_body:
        py_function.add_body_statement(statement)
    for variable in local_variables:
        py_function.add_local_variable(variable)


class ASTParser:
    def __init__(self, project):
        self.current_project = project
        self.current_module = None

    def parse_file(self, file_path, project_root):
        with open(file_path, 'r') as file:
            source_code = file.read()
        package_name = extract_package_name(file_path, project_root)
        self.current_module = PyModule(os.path.basename(file_path), package_name)
        self.current_project.add_module(self.current_module)
        tree = ast.parse(source_code)
        self.visit(tree)
        return self.current_module

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def visit_ClassDef(self, node):
        start_line = node.lineno
        end_line = max(child.lineno for child in ast.walk(node) if hasattr(child, 'lineno'))
        py_class = PyClass(node.name, start_line, end_line)
        self.current_module.add_class(py_class)
        self.current_project.hierarchy_graph.add_class(node.name)
        for base in node.bases:
            if isinstance(base, ast.Name):
                self.current_project.hierarchy_graph.add_inheritance(node.name, base.id)
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                py_method = self.visit_FunctionDef(item, py_class)
                py_class.add_method(py_method)
            # Add more logic here for other class contents
        return py_class

    def visit_FunctionDef(self, node, parent_class=None):
        start_line = node.lineno
        end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line

        # Handle return type
        return_type = get_return_type(node)

        # Handle function body and local variables
        function_body, local_variables = get_function_body_and_variables(node)

        if parent_class:  # It's a method in a class
            access_modifier = determine_access_modifier(node)
            decorators = get_decorators(node)
            py_method = PyMethod(node.name, start_line, end_line, access_modifier, decorators)
            populate_function_details(py_method, return_type, function_body, local_variables)
            for arg in node.args.args:
                param = self.visit_arg(arg)
                py_method.add_parameter(param)
            parent_class.add_method(py_method)
            return py_method
        else:  # It's a standalone function
            py_function = PyFunction(node.name, start_line, end_line)
            populate_function_details(py_function, return_type, function_body, local_variables)
            for arg in node.args.args:
                param = self.visit_arg(arg)
                py_function.add_parameter(param)
            self.current_module.add_function(py_function)
            return py_function

    def visit_Import(self, node):
        for alias in node.names:
            py_import = PyImport(alias.name, alias.asname)
            self.current_module.add_import(py_import)
            self.current_project.dependency_graph.add_dependency(self.current_module.name, alias.name)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            module_name = f"{node.module}.{alias.name}"
            py_import = PyImport(module_name, alias.asname, is_from_import=True)
            self.current_module.add_import(py_import)
            self.current_project.dependency_graph.add_dependency(self.current_module.name, module_name)

    def visit_arg(self, node):
        # Handle default values and type annotations if present
        default_value = None
        param_type = None
        if node.annotation:
            param_type = get_annotation(node.annotation)
        return PyParameter(node.arg, param_type, default_value)

    def generic_visit(self, node):
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)
