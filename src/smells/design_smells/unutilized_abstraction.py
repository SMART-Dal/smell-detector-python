import logging

from ..smell_detector import DesignSmellDetector


class UnutilizedAbstractionDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        smells = []
        try:
            for sm_class in module.classes:
                if self._is_unutilized_abstraction(sm_class, module):
                    detail = f"Class '{sm_class.name}' appears to be an unutilized abstraction."
                    smell = self._create_smell(module.name, sm_class, detail, sm_class.start_line)
                    if smell:
                        smells.append(smell)
        except Exception as e:
            logging.error(f"Error detecting unutilized abstractions in {module.name}: {e}", exc_info=True)
        return smells

    def _is_unutilized_abstraction(self, sm_class, module):
        # Check if the class is used anywhere in the module or project
        if not sm_class.is_used and not self._is_base_class(sm_class, module):
            return True
        return False

    @staticmethod
    def _is_base_class(sm_class, module):
        # Check if the class is a base class for other classes that are utilized
        for other_class in module.classes:
            if sm_class.name in other_class.super_classes and other_class.is_used:
                return True
        return False
