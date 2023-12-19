import pytest
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_method import SMMethod


# Fixture for creating a standard SMClass instance
@pytest.fixture
def sm_class_instance():
    return SMClass(name="TestClass", start_line=1, end_line=100)


# Fixture for creating a mock method object
@pytest.fixture
def method_mock(mocker):
    mock = mocker.MagicMock(spec=SMMethod, name="test_method")
    mock.name = "test_method"
    return mock


# Testing the initialization and basic properties of SMClass
def test_smclass_initialization(sm_class_instance):
    assert sm_class_instance.name == "TestClass", "The name should be initialized correctly"
    assert sm_class_instance.start_line == 1, "The start line should be initialized correctly"
    assert sm_class_instance.end_line == 100, "The end line should be initialized correctly"
    assert isinstance(sm_class_instance.methods, list), "Methods should be initialized to a list"
    assert isinstance(sm_class_instance.class_fields, dict), "Class fields should be initialized to a dictionary"
    assert isinstance(sm_class_instance.instance_fields, dict), "Instance fields should be initialized to a dictionary"


# Testing the addition of methods to the class
def test_add_method(sm_class_instance, method_mock):
    sm_class_instance.add_method(method_mock)
    assert method_mock in sm_class_instance.methods, "The method should be added to the class"


# Testing the registration of method interactions
def test_add_method_interaction(sm_class_instance, method_mock):
    sm_class_instance.add_method(method_mock)  # Add the method first
    field_name = "test_field"
    sm_class_instance.add_method_interaction(method_mock.name, field_name)
    assert field_name in sm_class_instance.method_interactions[
        method_mock.name], "The field should be registered as an interaction"


# Testing the addition of class-level fields
def test_add_class_field(sm_class_instance):
    field_name = "STATIC_FIELD"
    access_modifier = "public"
    sm_class_instance.add_class_field(field_name, access_modifier)
    assert sm_class_instance.class_fields[
               field_name] == access_modifier, "The class field with correct access modifier should be added"


# Testing the addition of instance-level fields
def test_add_instance_field(sm_class_instance):
    field_name = "instance_field"
    sm_class_instance.add_instance_field(field_name)
    assert sm_class_instance.instance_fields[
               field_name] == 'public', "The instance field should be added with public access by default"


# Testing the registration of external dependencies
def test_add_external_dependency(sm_class_instance):
    dependency = "external_module"
    sm_class_instance.add_external_dependency(dependency)
    assert dependency in sm_class_instance.external_dependencies, "The external dependency should be added to the class"

