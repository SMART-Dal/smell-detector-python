class PyFunction:
    def __init__(self, name, start_line, end_line, ast_node):
        self.name = name
        self.start_line = start_line
        self.end_line = end_line
        self.ast_node = ast_node
        self.parameters = []
        self.return_type = None
        self.function_body = []
        self.local_variables = []
        self.called_methods = set()

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    def set_return_type(self, return_type):
        self.return_type = return_type

    def add_body_statement(self, statement):
        self.function_body.append(statement)

    def add_local_variable(self, variable):
        self.local_variables.append(variable)

    def add_called_method(self, method_name):
        self.called_methods.add(method_name)

