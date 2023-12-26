import logging

from ..smell_detector import DesignSmellDetector


class UnnecessaryAbstractionDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        smells = []
        try:
            for py_class in module.classes:
                try:
                    if self._is_unnecessary_abstraction(py_class, config):
                        detail = f"Class '{py_class.name}' might represent an unnecessary abstraction with minimal functionality."
                        smell = self._create_smell(module.name, py_class, detail, py_class.start_line)
                        if smell:
                            smells.append(smell)
                except Exception as class_error:
                    logging.error(
                        f"Error checking Unnecessary Abstraction for class {py_class.name} in module {module.name}: {class_error}",
                        exc_info=True)

            logging.info(f"Detected {len(smells)} Unnecessary Abstraction smells in {module.name}")
        except Exception as module_error:
            logging.error(f"Error detecting Unnecessary Abstraction smells in module {module.name}: {module_error}",
                          exc_info=True)
        return smells

    @staticmethod
    def _is_unnecessary_abstraction(py_class, config):
        try:
            # Retrieve configuration values or set defaults
            max_methods = config.get('max_methods', 0)
            max_fields = config.get('max_fields', 1)
            min_method_loc = config.get('min_method_loc', 25)
            # Check for minimal methods and fields and no substantial methods
            if (len(py_class.methods) <= max_methods and
                    len(py_class.class_fields) + len(py_class.instance_fields) <= max_fields and
                    all(method.loc < min_method_loc for method in py_class.methods)):
                return True
            return False
        except Exception as error:
            logging.error(f"Error in _is_unnecessary_abstraction for class {py_class.name}: {error}", exc_info=True)
            return False
