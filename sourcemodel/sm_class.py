class PyClass:
    def __init__(self, name, start_line, end_line):
        self.name = name
        self.start_line = start_line
        self.end_line = end_line
        self.methods = []
        self.class_variables = []
        self.base_classes = []
        self.nested_classes = []

    def add_method(self, method_obj):
        self.methods.append(method_obj)

    def add_variable(self, variable_obj):
        self.class_variables.append(variable_obj)

    def add_nested_class(self, nested_class_obj):
        self.nested_classes.append(nested_class_obj)
