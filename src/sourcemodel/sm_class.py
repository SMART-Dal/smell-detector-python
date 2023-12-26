class SMClass:
    def __init__(self, name, start_line, end_line):
        self.name = name
        self.start_line = start_line
        self.end_line = end_line
        self.methods = []
        self.class_fields = {}  # Static fields
        self.instance_fields = {}  # Instance fields
        self.method_interactions = {}
        self.external_dependencies = set()
        self.lcom4 = None
        self.super_classes = []
        self.is_used = False

    def add_method(self, method_obj):
        self.methods.append(method_obj)
        if method_obj.name not in self.method_interactions:
            self.method_interactions[method_obj.name] = set()  # Initialize the set for the method
        # print(f"Added method: {method_obj.name}")

    def add_method_interaction(self, method_name, field_name):
        if method_name in self.method_interactions:
            self.method_interactions[method_name].add(field_name)

    def add_class_field(self, field_name, access_modifier):
        self.class_fields[field_name] = access_modifier

    def add_instance_field(self, field_name):
        # print(f"Adding instance field {field_name}")
        self.instance_fields[field_name] = 'public'  # Default to public for instance fields

    def add_external_dependency(self, dependency):
        self.external_dependencies.add(dependency)

    def set_metrics(self, lcom4):
        self.lcom4 = lcom4

    def mark_as_used(self):
        self.is_used = True

    def add_super_class(self, super_class_name):
        self.super_classes.append(super_class_name)
