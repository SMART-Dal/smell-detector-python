class SMFunction:
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
        self.used_modules = set()
        self.external_calls = set()
        self.loc = None
        self.complexity = None
        self.parameter_count = None

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
        if '.' in method_name:
            module_name = method_name.split('.')[0]
            self.used_modules.add(module_name)  # Add this line

    def add_external_call(self, called_name):
        self.external_calls.add(called_name)

    def set_metrics(self, loc, complexity, parameter_count):
        self.loc = loc
        self.complexity = complexity
        self.parameter_count = parameter_count
