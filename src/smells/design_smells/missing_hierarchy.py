import ast
import logging

from ..smell_detector import DesignSmellDetector


class MissingHierarchyDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        smells = []
        try:
            for py_class in module.classes:
                for method in py_class.methods:
                    if self._is_missing_hierarchy(method, config):
                        detail = f"Method '{method.name}' in class '{py_class.name}' may be missing a hierarchy to encapsulate variations."
                        smell = self._create_smell(module.name, py_class, detail, method.start_line)
                        if smell:
                            smells.append(smell)

            logging.info(f"Detected {len(smells)} Missing Hierarchy smells in {module.name}")
        except Exception as error:
            logging.error(f"Error detecting Missing Hierarchy smells in module {module.name}: {error}", exc_info=True)
        return smells

    def _is_missing_hierarchy(self, method, config):
        distinct_branches = self._count_distinct_branches(method.ast_node)
        threshold = config.get('max_branches', 3)  # Define a threshold for what's considered too many branches
        return distinct_branches > threshold

    def _count_distinct_branches(self, node):
        count = 0
        for child in ast.walk(node):
            if isinstance(child, ast.If):
                count += 1  # Count the initial if
                count += self._count_elif_branches(child)  # Add the count of 'elif' branches

            # Python 3.10+ match case statements
            elif isinstance(child, ast.Match):
                count += len(child.cases)
        return count

    @staticmethod
    def _count_elif_branches(node):
        # Recursively count the 'elif' branches in nested 'if' statements within the 'orelse' of an 'if'
        count = 0
        while isinstance(node.orelse, list) and len(node.orelse) == 1 and isinstance(node.orelse[0], ast.If):
            count += 1
            node = node.orelse[0]
        return count
