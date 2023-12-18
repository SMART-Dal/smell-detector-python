from src.sourcemodel.sm_function import SMFunction


class SMMethod(SMFunction):
    def __init__(self, name, start_line, end_line, access_modifier, decorators, ast_node):
        super().__init__(name, start_line, end_line, ast_node)
        self.access_modifier = access_modifier
        self.decorators = decorators
