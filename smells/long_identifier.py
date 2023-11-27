import ast


class LongIdentifierDetector(ast.NodeVisitor):
    def __init__(self, threshold=30):
        self.threshold = threshold
        self.long_identifiers = []

    def visit_ClassDef(self, node):
        if len(node.name) > self.threshold:
            self.long_identifiers.append(f"Class name too long: {node.name}")
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if len(node.name) > self.threshold:
            self.long_identifiers.append(f"Function name too long: {node.name}")
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name) and len(target.id) > self.threshold:
                self.long_identifiers.append(f"Variable name too long: {target.id}")
        self.generic_visit(node)


def detect_long_identifiers(code, threshold=30):
    tree = ast.parse(code)
    detector = LongIdentifierDetector(threshold)
    detector.visit(tree)
    return detector.long_identifiers


# Example usage
code = """
class ThisIsAnExampleOfAClassWithAnExtremelyLongName:
    def a_function_with_a_really_really_long_name(self):
        a_variable_with_an_extremely_long_name = 5
"""

long_identifiers = detect_long_identifiers(code)
for identifier in long_identifiers:
    print(identifier)
