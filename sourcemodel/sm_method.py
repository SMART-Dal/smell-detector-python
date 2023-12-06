from sourcemodel.sm_function import PyFunction


class PyMethod(PyFunction):
    def __init__(self, name, access_modifier, decorators):
        super().__init__(name)
        self.access_modifier = access_modifier
        self.decorators = decorators
