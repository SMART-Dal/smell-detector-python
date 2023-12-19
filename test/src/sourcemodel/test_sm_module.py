import pytest
from pytest_mock import mocker

from src.sourcemodel.dependency_graph import DependencyGraph
from src.sourcemodel.sm_class import SMClass
from src.sourcemodel.sm_function import SMFunction
from src.sourcemodel.sm_module import SMModule


# Mocks for the metrics calculations
@pytest.fixture
def mock_metrics(mocker):
    mocker.patch('src.metrics.calculate_module_loc', return_value=100)
    mocker.patch('src.metrics.calculate_wmc_for_module', return_value=10)
    mocker.patch('src.metrics.calculate_nom', return_value=5)
    mocker.patch('src.metrics.calculate_nopm', return_value=3)
    mocker.patch('src.metrics.calculate_nof', return_value=2)
    mocker.patch('src.metrics.calculate_nopf', return_value=1)
    mocker.patch('src.metrics.calculate_lcom4', return_value=0)
    mocker.patch('src.metrics.calculate_fan_in_class', return_value=4)
    mocker.patch('src.metrics.calculate_fan_out_class', return_value=4)


@pytest.fixture
def module_instance():
    dependency_graph = DependencyGraph()
    return SMModule(name="TestModule", package_name="TestPackage", input_dependency_graph=dependency_graph)


def test_add_class(module_instance):
    sm_class = SMClass(name="TestClass", start_line=1, end_line=20)
    module_instance.add_class(sm_class)
    assert sm_class in module_instance.classes, "The class should be added to the module"


def test_add_function(module_instance, mocker):
    ast_node_mock = mocker.MagicMock()
    sm_function = SMFunction(name="test_function", start_line=1, end_line=10, ast_node=ast_node_mock)
    module_instance.add_function(sm_function)
    assert sm_function in module_instance.functions, "The function should be added to the module"


def test_add_import(module_instance):
    sm_import = 'import os'
    module_instance.add_import(sm_import)
    assert sm_import in module_instance.imports, "The import should be added to the module"


def test_add_global_variable(module_instance):
    global_variable = 'TEST_VARIABLE'
    module_instance.add_global_variable(global_variable)
    assert global_variable in module_instance.global_variables, "The global variable should be added to the module"


def test_analyze(module_instance, mock_metrics, mocker):
    sm_class = SMClass(name="TestClass", start_line=1, end_line=10)
    module_instance.add_class(sm_class)
    ast_node_mock = mocker.MagicMock()
    sm_function = SMFunction(name="test_function", start_line= 2, end_line=9, ast_node=ast_node_mock)
    module_instance.add_function(sm_function)

    # Perform analysis
    analysis_result = module_instance.analyze()

    # Check for the expected keys in the results
    assert 'module_metrics' in analysis_result, "Analysis result should contain module metrics"
    assert 'class_metrics' in analysis_result, "Analysis result should contain class metrics"
    assert 'method_metrics' in analysis_result, "Analysis result should contain method metrics"
    assert 'function_metrics' in analysis_result, "Analysis result should contain function metrics"

    # Check for the correct calculation of metrics
    assert analysis_result['module_metrics']['loc'] == 100, "LOC should be calculated correctly"
    assert analysis_result['module_metrics']['wmc'] == 10, "WMC should be calculated correctly"
