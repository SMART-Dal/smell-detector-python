import logging

from ..smell_detector import DesignSmellDetector


class ImperativeAbstractionDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        smells = []
        try:
            # Iterate through each class in the module
            for py_class in module.classes:
                try:
                    if self._is_imperative_abstraction(py_class, config):
                        detail = f"Class '{py_class.name}' is potentially an imperative abstraction due to a single large public method and few class fields."
                        smell = self._create_smell(module.name, py_class, detail, py_class.start_line)
                        if smell:
                            smells.append(smell)
                except Exception as class_error:
                    logging.error(
                        f"Error checking Imperative Abstraction for class {py_class.name} in module {module.name}: {class_error}",
                        exc_info=True)

            logging.info(f"Detected {len(smells)} Imperative Abstraction smells in {module.name}")
        except Exception as module_error:
            logging.error(f"Error detecting Imperative Abstraction smells in module {module.name}: {module_error}",
                          exc_info=True)
        return smells

    @staticmethod
    def _is_imperative_abstraction(py_class, config):
        try:
            # Retrieve configuration values or set defaults
            max_fields = config.get('threshold', 3)
            large_method_line_threshold = config.get('max_line', 50)

            # Find public methods in the class
            public_methods = [method for method in py_class.methods if method.access_modifier == 'public']

            # Check for a single public method and minimal fields
            if (len(public_methods) == 1 and
                    public_methods[0].loc > large_method_line_threshold and
                    len(py_class.class_fields) + len(py_class.instance_fields) <= max_fields):
                return True
            return False
        except Exception as error:
            logging.error(f"Error checking Imperative Abstraction for class {py_class.name}: {error}", exc_info=True)
            return False
