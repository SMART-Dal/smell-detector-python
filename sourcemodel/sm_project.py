class PyProject:
    def __init__(self):
        self.modules = []

    def add_module(self, module):
        self.modules.append(module)

    def analyze_project(self):
        for module in self.modules:
            module.analyze()




