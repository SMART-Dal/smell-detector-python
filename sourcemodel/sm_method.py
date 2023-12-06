from sourcemodel.sm_function import PyFunction


class PyMethod(PyFunction):
    def __init__(self, name, start_line, end_line, access_modifier, decorators):
        super().__init__(name, start_line, end_line)
        self.access_modifier = access_modifier
        self.decorators = decorators
