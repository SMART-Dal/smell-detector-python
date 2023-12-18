class SMImport:
    def __init__(self, module_name, alias=None, is_from_import=False):
        self.module_name = module_name
        self.alias = alias
        self.is_from_import = is_from_import
