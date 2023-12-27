import logging

from ..smell_detector import DesignSmellDetector


class WideHierarchyDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        smells = []
        try:
            wide_hierarchy_threshold = config.get('threshold', 5)
            hierarchy_graph = module.project.hierarchy_graph

            # Filter classes relevant to the current module
            relevant_classes = self._get_classes_in_module(module)

            for class_name in relevant_classes:
                children = list(hierarchy_graph.graph.successors(class_name))
                if len(children) > wide_hierarchy_threshold:
                    py_class = self._find_class_by_name(class_name, module)
                    if py_class:
                        detail = f"Class '{class_name}' has a wide hierarchy with {len(children)} direct subclasses."
                        smell = self._create_smell(module.name, py_class, detail)
                        if smell:
                            smells.append(smell)

            logging.info(f"Detected {len(smells)} Wide Hierarchy smells in {module.name}")
        except Exception as error:
            logging.error(f"Error detecting Wide Hierarchy smells in module {module.name}: {error}", exc_info=True)
        return smells

    @staticmethod
    def _get_classes_in_module(module):
        return [py_class.name for py_class in module.classes]

    @staticmethod
    def _find_class_by_name(class_name, module):
        for py_class in module.classes:
            if py_class.name == class_name:
                return py_class
        return None


