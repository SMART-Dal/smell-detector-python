import logging

from ..smell_detector import DesignSmellDetector


class DeepHierarchyDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        smells = []
        max_depth = config.get('max_depth', 4)  # Default or configurable depth

        try:
            for sm_class in module.classes:
                try:
                    depth = module.project.hierarchy_graph.get_inheritance_depth(sm_class.name)
                    if depth > max_depth:
                        detail = f"Class '{sm_class.name}' exceeds max depth with a depth of {depth}."
                        smell = self._create_smell(module.name, sm_class, detail, sm_class.start_line)
                        smells.append(smell)
                except Exception as e:
                    logging.error(f"Error calculating depth for class {sm_class.name} in module {module.name}: {e}", exc_info=True)
        except Exception as e:
            logging.error(f"Error detecting Deep Hierarchy smells in module {module.name}: {e}", exc_info=True)

        return smells
