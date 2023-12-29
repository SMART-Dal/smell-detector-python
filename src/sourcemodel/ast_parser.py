import ast
import logging
import os

from src.sourcemodel.ast_utils import extract_package_name, get_return_type, get_function_body_and_variables, \
    get_annotation
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_function import SMFunction
from src.sourcemodel.sm_import import SMImport
from src.sourcemodel.sm_method import SMMethod
from src.sourcemodel.sm_module import SMModule
from src.sourcemodel.sm_parameter import SMParameter


class ASTParser:
    def __init__(self, project):
        self.current_project = project
        self.current_module = None

    def parse(self, file_path, project_root):
        try:
            source_code = self._read_file(file_path)
            package_name = extract_package_name(file_path, project_root)
            self.current_module = SMModule(os.path.basename(file_path), self.current_project, package_name)
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
        sm_class = self._create_sm_class(node)
        self.current_module.add_class(sm_class)
        self.current_project.hierarchy_graph.add_class(node.name)

        for base in node.bases:
            if isinstance(base, ast.Name):
                base_class_name = base.id
                sm_class.add_super_class(base_class_name)
                self.current_project.hierarchy_graph.add_inheritance(node.name, base_class_name)
                base_class = self.current_project.find_class(base_class_name)
                if base_class:
                    base_class.mark_as_used()

        self._process_class_body(sm_class, node.body)
        return sm_class

    def visit_Call(self, node):
        # When visiting calls, check if it's a class instantiation or method call
        if isinstance(node.func, ast.Name):
            called_name = node.func.id
            self._mark_class_used(called_name)
        elif isinstance(node.func, ast.Attribute):
            # This could be a method call; mark the class of the method as used
            if isinstance(node.func.value, ast.Name):
                class_name = node.func.value.id
                self._mark_class_used(class_name)

    def _mark_class_used(self, class_name):
        # Logic to mark a class as used
        for module in self.current_project.modules:
            for sm_class in module.classes:
                if sm_class.name == class_name:
                    sm_class.mark_as_used()
                    break

    def _create_sm_class(self, node):
        start_line, end_line = node.lineno, self._get_end_line(node)
        return SMClass(node.name, start_line, end_line)

    def _process_class_body(self, sm_class, body):
        for item in body:
            if isinstance(item, ast.FunctionDef):
                self.visit_FunctionDef(item, sm_class)
            elif isinstance(item, ast.Assign):
                self._process_class_variables(sm_class, item)

    @staticmethod
    def _process_class_variables(sm_class, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                access_modifier = 'public' if not target.id.startswith('_') else 'private'
                sm_class.add_class_field(target.id, access_modifier)

    def visit_FunctionDef(self, node, parent_class=None):
        sm_function = self._create_sm_function_or_method(node, parent_class)
        if parent_class:
            parent_class.add_method(sm_function)
            for stmt in ast.walk(node):
                if isinstance(stmt, ast.Assign):
                    for target in stmt.targets:
                        if isinstance(target, ast.Attribute) and isinstance(target.value,
                                                                            ast.Name) and target.value.id == 'self':
                            parent_class.add_instance_field(target.attr)
            self._analyze_function_body(node, sm_function, parent_class)
        else:
            self.current_module.add_function(sm_function)
        return sm_function

    def _create_sm_function_or_method(self, node, parent_class):
        start_line, end_line = node.lineno, self._get_end_line(node)
        return_type, function_body, local_variables = self._process_function_details(node)
        parameters = [self.visit_arg(arg) for arg in node.args.args]

        if parent_class:
            access_modifier = 'public' if not node.name.startswith('_') else 'private'
            decorators = self._get_decorators(node)
            sm_method = SMMethod(node.name, start_line, end_line, access_modifier, decorators, node)
            self._populate_function_details(sm_method, return_type, function_body, local_variables, parameters)
            return sm_method
        else:
            sm_function = SMFunction(node.name, start_line, end_line, node)
            self._populate_function_details(sm_function, return_type, function_body, local_variables, parameters)
            return sm_function

    def _analyze_function_body(self, node, sm_function, parent_class):
        if parent_class:
            for stmt in ast.walk(node):
                # Check for method interactions within the class (for fan-in)
                if isinstance(stmt, ast.Attribute) and isinstance(stmt.value, ast.Name) and stmt.value.id == 'self':
                    field_name = stmt.attr
                    if field_name in parent_class.class_fields or field_name in parent_class.instance_fields:
                        parent_class.add_method_interaction(sm_function.name, field_name)

                if isinstance(stmt, ast.Call):
                    called_name = None
                    # Direct function calls (e.g., some_function())
                    if isinstance(stmt.func, ast.Name):
                        called_name = stmt.func.id
                        self._mark_class_as_used(called_name)
                    # Method calls or attribute access on an object (e.g., some_object.some_method())
                    elif isinstance(stmt.func, ast.Attribute) and isinstance(stmt.func.value, ast.Name):
                        called_name = f"{stmt.func.value.id}.{stmt.func.attr}"

                    # If a called name was identified, add it as an external call
                    if called_name:
                        sm_function.add_external_call(called_name)
                        # If this is a method within a class, also note the external dependency at the class level
                        if parent_class:
                            parent_class.add_external_dependency(called_name.split('.')[0])

    @staticmethod
    def _get_decorators(node):
        return [decorator.id for decorator in node.decorator_list if isinstance(decorator, ast.Name)]

    @staticmethod
    def _populate_function_details(sm_function, return_type, function_body, local_variables, parameters):
        sm_function.set_return_type(return_type)
        sm_function.parameters = parameters
        for statement in function_body:
            sm_function.add_body_statement(statement)
        for variable in local_variables:
            sm_function.add_local_variable(variable)

    @staticmethod
    def _process_function_details(node):
        return_type = get_return_type(node)
        function_body, local_variables = get_function_body_and_variables(node)
        return return_type, function_body, local_variables

    def _mark_class_as_used(self, class_name):
        sm_class = self.current_project.find_class(class_name)
        if sm_class:
            sm_class.mark_as_used()

    def visit_Import(self, node):
        for alias in node.names:
            sm_import = SMImport(alias.name, alias.asname)
            self.current_module.add_import(sm_import)
            self.current_project.dependency_graph.add_dependency(self.current_module.name, alias.name)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            module_name = f"{node.module}.{alias.name}"
            sm_import = SMImport(module_name, alias.asname, is_from_import=True)
            self.current_module.add_import(sm_import)
            self.current_project.dependency_graph.add_dependency(self.current_module.name, module_name)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name):
                self.current_module.add_global_variable(target.id)

    @staticmethod
    def visit_arg(node):
        default_value = None
        param_type = get_annotation(node.annotation) if node.annotation else None
        return SMParameter(node.arg, param_type, default_value)

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
