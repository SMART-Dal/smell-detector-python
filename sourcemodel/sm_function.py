class PyFunction:
    def __init__(self, name):
        self.name = name
        self.parameters = []
        self.return_type = None
        self.function_body = []
        self.local_variables = []

    def add_parameter(self, parameter):
        self.parameters.append(parameter)

    def set_return_type(self, return_type):
        self.return_type = return_type

    def add_body_statement(self, statement):
        self.function_body.append(statement)

    def add_local_variable(self, variable):
        self.local_variables.append(variable)
