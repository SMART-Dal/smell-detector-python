import logging
from collections import defaultdict

from ..smell_detector import DesignSmellDetector


class BrokenModularizationDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        smells = []
        try:
            cross_reference_map = self._build_cross_reference_map(module)
            for py_class in module.classes:
                if self._is_broken_modularization(py_class, cross_reference_map, config):
                    detail = f"Class '{py_class.name}' seems to be part of broken modularization."
                    smell = self._create_smell(module.name, py_class, detail, py_class.start_line)
                    if smell:
                        smells.append(smell)

            logging.info(f"Detected {len(smells)} Broken Modularization smells in {module.name}")
        except Exception as error:
            logging.error(f"Error detecting Broken Modularization smells in module {module.name}: {error}",
                          exc_info=True)
        return smells

    @staticmethod
    def _build_cross_reference_map(module):
        reference_map = defaultdict(set)
        for py_class in module.classes:
            for method in py_class.methods:
                for external_call in method.external_calls:
                    reference_map[py_class.name].add(external_call.split('.')[0])
        return reference_map

    @staticmethod
    def _is_broken_modularization(py_class, cross_reference_map, config):
        threshold = config.get('x_references', 5)
        external_references = cross_reference_map[py_class.name]
        if len(external_references) > threshold:
            return True
        return False
