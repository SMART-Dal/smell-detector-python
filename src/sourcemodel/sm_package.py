class SMPackage:
    def __init__(self, name):
        self.name = name
        self.modules = []

    def add_module(self, module):
        self.modules.append(module)

    def analyze(self):
        for module in self.modules:
            module.analyze()
