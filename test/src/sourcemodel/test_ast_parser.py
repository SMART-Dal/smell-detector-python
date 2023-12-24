import ast
import pytest
from unittest.mock import MagicMock
from src.sourcemodel.ast_parser import ASTParser
from src.sourcemodel.sm_project import SMProject
from src.sourcemodel.sm_module import SMModule
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_method import SMMethod
from src.sourcemodel.sm_import import SMImport

# Sample Python code for testing
sample_code = """
class SampleClass:
    def sample_method(self, arg):
        if arg:
            print(arg)
"""


@pytest.fixture
def mock_project():
    project = MagicMock(spec=SMProject)
    project.dependency_graph = MagicMock()
    project.hierarchy_graph = MagicMock()
    return project


@pytest.fixture
def mock_module():
    return MagicMock(spec=SMModule)


@pytest.fixture
def ast_parser_instance(mock_project):
    return ASTParser(mock_project)


@pytest.fixture
def sample_ast_tree():
    return ast.parse(sample_code)


def test_parse(ast_parser_instance, mocker):
    # Setup
    mocker.patch('src.sourcemodel.ast_parser.ASTParser._read_file', return_value=sample_code)
    mocker.patch('os.path.basename', return_value='sample.py')
    mocker.patch('src.sourcemodel.ast_parser.extract_package_name', return_value='sample_package')

    # Execution
    result = ast_parser_instance.parse('path/to/sample.py', 'path/to')

    # Assertion
    assert isinstance(result, SMModule), "Should return an SMModule instance"


def test_visit_ClassDef(ast_parser_instance, sample_ast_tree, mocker):
    # Setup
    class_node = sample_ast_tree.body[0]
    mock_module = SMModule('sample.py', 'sample_package')
    ast_parser_instance.current_module = mock_module

    # Execution
    result = ast_parser_instance.visit_ClassDef(class_node)

    # Assertions
    assert isinstance(result, SMClass), "Should return an SMClass instance"
    assert result.name == "SampleClass", "The class name should be SampleClass"


def test_parse_error_handling(ast_parser_instance, mocker):
    # Setup
    mocker.patch('src.sourcemodel.ast_parser.ASTParser._read_file', side_effect=Exception("Error reading file"))

    # Execution
    result = ast_parser_instance.parse('path/to/invalid.py', 'path/to')

    # Assertion
    assert result is None, "Should return None on error"


def test_visit_FunctionDef(ast_parser_instance, sample_ast_tree, mocker):
    # Setup
    function_node = sample_ast_tree.body[0].body[0]
    mock_class = SMClass('SampleClass', 1, 10)
    mock_method = SMMethod('sample_method', 2, 5, 'public', [], function_node)

    # Mock the internal method to return a specific SMMethod instance
    mocker.patch.object(ast_parser_instance, '_create_sm_function_or_method', return_value=mock_method)

    # Execution
    result = ast_parser_instance.visit_FunctionDef(function_node, parent_class=mock_class)

    # Assertions
    assert isinstance(result, SMMethod), "Should return an SMMethod instance"
    assert result.name == "sample_method", "The method name should be sample_method"


def test_visit_Import(ast_parser_instance, mocker):
    # Setup
    import_node = ast.parse("import os").body[0]
    ast_parser_instance.current_module = SMModule('sample.py', 'sample_package')

    # Execution
    ast_parser_instance.visit_Import(import_node)

    # Assertions
    assert len(ast_parser_instance.current_module.imports) == 1, "Should have one import"
    assert isinstance(ast_parser_instance.current_module.imports[0], SMImport), "Should create an SMImport instance"


# Add more tests for other methods...

if __name__ == '__main__':
    pytest.main()
