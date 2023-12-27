import logging

from ..smell_detector import DesignSmellDetector


class BrokenHierarchyDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        smells = []
        try:
            for py_class in module.classes:
                if self.has_superclass(py_class):
                    for super_class_name in py_class.super_classes:
                        super_class = module.project.find_class(super_class_name)
                        if super_class and self._is_broken_hierarchy(py_class, super_class):
                            detail = f"Class '{py_class.name}' and its superclass '{super_class.name}' may not share a proper 'IS-A' relationship."
                            smell = self._create_smell(module.name, py_class, detail, py_class.start_line)
                            if smell:
                                smells.append(smell)
            logging.info(f"Detected {len(smells)} Broken Hierarchy smells in {module.name}")
        except Exception as error:
            logging.error(f"Error detecting Broken Hierarchy smells in module {module.name}: {error}", exc_info=True)
        return smells

    def _is_broken_hierarchy(self, subclass, superclass):
        for method in subclass.methods:
            super_method = self.find_method_in_class(method.name, superclass)
            if super_method and not self.is_behavior_consistent(method, super_method):
                return True  # Broken hierarchy detected
        return False

    @staticmethod
    def find_method_in_class(method_name, sm_class):
        for method in sm_class.methods:
            if method.name == method_name:
                return method
        return None

    def is_behavior_consistent(self, sub_method, super_method):
        if not self.is_signature_consistent(sub_method, super_method):
            return False
        return True

    @staticmethod
    def is_signature_consistent(sub_method, super_method):
        if len(sub_method.parameters) != len(super_method.parameters):
            return False
        for sub_param, super_param in zip(sub_method.parameters, super_method.parameters):
            if sub_param.param_type != super_param.param_type:
                return False
        if sub_method.return_type != super_method.return_type:
            return False
        return True

    @staticmethod
    def has_superclass(py_class):
        return len(py_class.super_classes) > 0
