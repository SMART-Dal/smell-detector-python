import ast
import logging
import os

from log_config import setup_logging
from sourcemodel import (
    PyClass, PyFunction, PyImport, PyMethod, PyModule, PyParameter
)
from sourcemodel.ast_utils import (
    get_return_type, get_function_body_and_variables, get_annotation, extract_package_name
)

setup_logging()


class ASTParser:
    def __init__(self, project):
        self.current_project = project
        self.current_module = None

    def parse(self, file_path, project_root):
        try:
            source_code = self._read_file(file_path)
            package_name = extract_package_name(file_path, project_root)
            self.current_module = PyModule(os.path.basename(file_path), package_name)
            self.current_project.add_module(self.current_module)
            self.current_project.dependency_graph.add_module(self.current_module.name)
            tree = ast.parse(source_code)
            self._visit(tree)
        except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}")
            return None
        return self.current_module

    @staticmethod
    def _read_file(file_path):
        with open(file_path, 'r') as file:
            return file.read()

    def _visit(self, node):
        method_name = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method_name, self._generic_visit)
        return visitor(node)

    def visit_ClassDef(self, node):
        py_class = self._create_py_class(node)
        self.current_module.add_class(py_class)
        self.current_project.hierarchy_graph.add_class(node.name)

        for base in node.bases:
            if isinstance(base, ast.Name):
                base_class_name = base.id
                self.current_project.hierarchy_graph.add_inheritance(node.name, base_class_name)

        self._process_class_body(py_class, node.body)
        return py_class

    def _create_py_class(self, node):
        start_line, end_line = node.lineno, self._get_end_line(node)
        return PyClass(node.name, start_line, end_line)

    def _process_class_body(self, py_class, body):
        for item in body:
            if isinstance(item, ast.FunctionDef):
                self.visit_FunctionDef(item, py_class)
            elif isinstance(item, ast.Assign):
                self._process_class_variables(py_class, item)

    @staticmethod
    def _process_class_variables(py_class, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                access_modifier = 'public' if not target.id.startswith('_') else 'private'
                py_class.add_class_field(target.id, access_modifier)

    def visit_FunctionDef(self, node, parent_class=None):
        py_function = self._create_py_function_or_method(node, parent_class)
        if parent_class:
            parent_class.add_method(py_function)
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Assign):
                    for target in stmt.targets:
                        if isinstance(target, ast.Attribute) and isinstance(target.value,
                                                                            ast.Name) and target.value.id == 'self':
                            parent_class.add_instance_field(target.attr)
            self._analyze_function_body(node, py_function, parent_class)
        else:
            self.current_module.add_function(py_function)
        return py_function

    def _create_py_function_or_method(self, node, parent_class):
        start_line, end_line = node.lineno, self._get_end_line(node)
        return_type, function_body, local_variables = self._process_function_details(node)
        parameters = [self.visit_arg(arg) for arg in node.args.args]

        if parent_class:
            access_modifier = 'public' if not node.name.startswith('_') else 'private'
            decorators = self._get_decorators(node)
            py_method = PyMethod(node.name, start_line, end_line, access_modifier, decorators, node)
            self._populate_function_details(py_method, return_type, function_body, local_variables, parameters)
            return py_method
        else:
            py_function = PyFunction(node.name, start_line, end_line, node)
            self._populate_function_details(py_function, return_type, function_body, local_variables, parameters)
            return py_function

    @staticmethod
    def _analyze_function_body(node, py_function, parent_class):
        if parent_class:
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Attribute) and isinstance(stmt.value, ast.Name) and stmt.value.id == 'self':
                    field_name = stmt.attr
                    if field_name in parent_class.class_fields or field_name in parent_class.instance_fields:
                        parent_class.add_method_interaction(py_function.name, field_name)

    @staticmethod
    def _get_decorators(node):
        return [decorator.id for decorator in node.decorator_list if isinstance(decorator, ast.Name)]

    @staticmethod
    def _populate_function_details(py_function, return_type, function_body, local_variables, parameters):
        py_function.set_return_type(return_type)
        py_function.parameters = parameters
        for statement in function_body:
            py_function.add_body_statement(statement)
        for variable in local_variables:
            py_function.add_local_variable(variable)

    @staticmethod
    def _process_function_details(node):
        return_type = get_return_type(node)
        function_body, local_variables = get_function_body_and_variables(node)
        return return_type, function_body, local_variables

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

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.current_module.add_global_variable(target.id)

    @staticmethod
    def visit_arg(node):
        default_value = None
        param_type = get_annotation(node.annotation) if node.annotation else None
        return PyParameter(node.arg, param_type, default_value)

    def _generic_visit(self, node):
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self._visit(item)
            elif isinstance(value, ast.AST):
                self._visit(value)

    @staticmethod
    def _get_end_line(node):
        return max(child.lineno for child in ast.walk(node) if hasattr(child, 'lineno'))
