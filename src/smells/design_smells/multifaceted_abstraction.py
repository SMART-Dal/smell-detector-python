import logging

from ..smell_detector import DesignSmellDetector


class MultifacetedAbstractionDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        smells = []
        max_lcom = config.get("max_lcom", 1.5)  # Default LCOM4 threshold for multifaceted abstraction
        min_methods = config.get("min_methods", 3)  # Minimum number of methods to consider a class for this smell

        for py_class in module.classes:
            try:
                lcom4 = py_class.metrics['lcom4']
                if lcom4 > max_lcom and len(py_class.methods) >= min_methods:
                    detail = f"Class '{py_class.name}' has a high LCOM4 value of {lcom4}, indicating it may have multiple responsibilities."
                    smell = self._create_smell(module.name, py_class, detail, py_class.start_line)
                    if smell:
                        smells.append(smell)
            except Exception as e:
                logging.error(
                    f"Error detecting Multifaceted Abstraction in class {py_class.name} of module {module.name}: {e}",
                    exc_info=True)

        return smells
