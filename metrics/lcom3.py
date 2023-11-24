import ast
import logging

from collections import defaultdict

from log_config import setup_logging

# Configure logging
setup_logging()


class LCOM3Calculator:
    def __init__(self, class_node):
        self.class_node = class_node
        self.method_fields = defaultdict(set)
        self.fields = set()
        logging.debug(f"Initializing LCOM3Calculator for class: {class_node.name}")

    def calculate(self):
        logging.debug("Starting LCOM3 calculation")
        self._extract_fields()
        self._extract_method_fields()
        lcom3_value = self._compute_lcom3()
        logging.debug(f"Completed LCOM3 calculation: {lcom3_value}")
        return lcom3_value

    def _extract_fields(self):
        logging.debug("Extracting fields from class")
        for node in ast.walk(self.class_node):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Attribute) and isinstance(target.value, ast.Name):
                        if target.value.id == 'self':
                            self.fields.add(target.attr)
                            logging.debug(f"Found field: {target.attr}")

    def _extract_method_fields(self):
        logging.debug("Extracting method-field interactions")
        for node in self.class_node.body:
            if isinstance(node, ast.FunctionDef) and node.name != '__init__':
                method_name = node.name
                self.method_fields[method_name] = {
                    sub_node.attr for sub_node in ast.walk(node)
                    if isinstance(sub_node, ast.Attribute) and isinstance(sub_node.value, ast.Name)
                    and sub_node.value.id == 'self' and sub_node.attr in self.fields
                }
                logging.debug(f"Method {method_name} accesses fields: {self.method_fields[method_name]}")

    def _compute_lcom3(self):
        logging.debug("Computing LCOM3")
        methods = list(self.method_fields.keys())
        p, q = 0, 0
        for i in range(len(methods)):
            for j in range(i + 1, len(methods)):
                fields_i = self.method_fields[methods[i]]
                fields_j = self.method_fields[methods[j]]
                if fields_i.isdisjoint(fields_j):
                    p += 1
                    logging.debug(f"Unshared pair: {methods[i]} - {methods[j]}")
                elif fields_i.intersection(fields_j):
                    q += 1
                    logging.debug(f"Shared pair: {methods[i]} - {methods[j]}")

        logging.debug(f"Shared pairs (Q): {q}, Unshared pairs (P): {p}")
        if q == 0 and p > 0:
            return 1
        if p == 0 and q == 0:
            return None

        lcom3_value = p / (p + q) if p + q > 0 else 0
        logging.debug(f"LCOM3 Value: {lcom3_value}")
        return lcom3_value


def calculate_lcom3(class_node):
    if not isinstance(class_node, ast.ClassDef):
        logging.warning("LCOM3 calculation is applicable only to class definitions.")
        return None
    logging.info(f"Calculating LCOM3 for class: {class_node.name}")
    calculator = LCOM3Calculator(class_node)
    return calculator.calculate()
