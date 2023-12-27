import ast
import logging

from ..smell_detector import DesignSmellDetector


class RebelliousHierarchyDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        project = module.project
        smells = []
        try:
            for py_class in module.classes:
                try:
                    if self.has_superclass(py_class) and self._has_rebellious_methods(py_class, project):
                        detail = f"Class '{py_class.name}' potentially exhibits a rebellious hierarchy by not properly utilizing superclass methods."
                        smell = self._create_smell(module.name, py_class, detail, py_class.start_line)
                        if smell:
                            smells.append(smell)
                except Exception as class_error:
                    logging.error(
                        f"Error checking Rebellious Hierarchy for class {py_class.name} in module {module.name}: {class_error}",
                        exc_info=True)

            logging.info(f"Detected {len(smells)} Rebellious Hierarchy smells in {module.name}")
        except Exception as module_error:
            logging.error(f"Error detecting Rebellious Hierarchy smells in module {module.name}: {module_error}",
                          exc_info=True)
        return smells

    @staticmethod
    def has_superclass(py_class):
        return len(py_class.super_classes) > 0

    def _has_rebellious_methods(self, py_class, project):
        for method in py_class.methods:
            if self.is_method_rebellious(method, py_class, project):
                return True
        return False

    def is_method_rebellious(self, method, sm_class, project):
        for super_class_name in sm_class.super_classes:
            super_class = project.find_class(super_class_name)
            if super_class:
                super_method = self.find_method_in_class(method.name, super_class)
                if super_method and self.is_implementation_trivial(method):
                    return True  # Method is rebellious
        return False

    @staticmethod
    def find_method_in_class(method_name, sm_class):
        for method in sm_class.methods:
            if method.name == method_name:
                return method
        return None

    @staticmethod
    def is_implementation_trivial(method):
        # Analyze the method's AST to check if it's trivial or empty
        # This could be looking for empty bodies, only a pass statement, or just a raise/return statement
        for node in ast.walk(method.ast_node):
            if isinstance(node, (ast.Raise, ast.Pass, ast.Return)):
                return True
        return False
