import ast


class LongIdentifierDetector(ast.NodeVisitor):
    def __init__(self, threshold=25):
        self.threshold = threshold
        self.long_identifiers = []

    def visit_ClassDef(self, node):
        if len(node.name) > self.threshold:
            self.long_identifiers.append(node.name)
        self.generic_visit(node)

    def visit_FunctionDef(self, node):
        if len(node.name) > self.threshold:
            self.long_identifiers.append(node.name)
        self.generic_visit(node)

    def visit_Assign(self, node):
        for target in node.targets:
            if isinstance(target, ast.Name) and len(target.id) > self.threshold:
                self.long_identifiers.append(target.id)
        self.generic_visit(node)


def detect_long_identifiers(code, threshold=25):
    tree = ast.parse(code)
    detector = LongIdentifierDetector(threshold)
    detector.visit(tree)
    return detector.long_identifiers
