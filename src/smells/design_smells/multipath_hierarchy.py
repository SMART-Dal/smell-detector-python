import logging

from ..smell_detector import DesignSmellDetector


class MultipathHierarchyDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        smells = []
        try:
            for sm_class in module.classes:
                has_multipath, ancestor = module.project.hierarchy_graph.has_multipath_inheritance(sm_class.name)
                if has_multipath:
                    detail = f"Class '{sm_class.name}' has multipath inheritance from '{ancestor}'."
                    smell = self._create_smell(module.name, sm_class, detail, sm_class.start_line)
                    if smell:
                        smells.append(smell)
        except Exception as e:
            logging.error(f"Error detecting Multipath Hierarchy smells in {module.name}: {e}", exc_info=True)
        return smells
