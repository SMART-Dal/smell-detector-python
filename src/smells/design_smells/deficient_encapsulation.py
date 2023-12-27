import ast
import logging

from ..smell_detector import DesignSmellDetector


class DeficientEncapsulationDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        smells = []
        try:
            for py_class in module.classes:
                for field_name, access_modifier in {**py_class.class_fields, **py_class.instance_fields}.items():
                    if self.is_deficiently_encapsulated(field_name, access_modifier, py_class, module):
                        detail = f"Field '{field_name}' in class '{py_class.name}' may be overly permissive."
                        smell = self._create_smell(module.name, py_class, detail, py_class.start_line)
                        if smell:
                            smells.append(smell)

            logging.info(f"Detected {len(smells)} Deficient Encapsulation smells in {module.name}")
        except Exception as error:
            logging.error(f"Error detecting Deficient Encapsulation smells in module {module.name}: {error}", exc_info=True)
        return smells

    def is_deficiently_encapsulated(self, name, access_modifier, py_class, module):
        if access_modifier == 'public' and not name.startswith('_'):  # Convention for non-public in Python
            return not self.is_used_appropriately(name, py_class, module)
        return False

    def is_used_appropriately(self, field_name, py_class, module):
        for other_class in module.classes:
            if other_class != py_class and self.is_field_accessed(field_name, other_class):
                return False
        return True

    @staticmethod
    def is_field_accessed(field_name, py_class):
        for method in py_class.methods:
            for node in ast.walk(method.ast_node):
                if isinstance(node, ast.Attribute) and node.attr == field_name:
                    return True
        return False
