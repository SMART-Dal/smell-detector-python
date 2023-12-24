import pytest
import logging

from src.smells.smell_detector import ImplementationSmellDetector, DesignSmellDetector


class ConcreteImplementationSmellDetector(ImplementationSmellDetector):
    def _detect_smells(self, module, config):
        if config.get('detect'):
            return [{'smell': 'detected'}]
        return []


class ConcreteDesignSmellDetector(DesignSmellDetector):
    def _detect_smells(self, module, config):
        if config.get('detect'):
            return [{'smell': 'detected'}]
        return []


@pytest.fixture
def module_mock(mocker):
    module = mocker.MagicMock()
    module.name = "test_module"
    module.functions = []
    module.classes = []
    return module


@pytest.fixture
def config_mock():
    return {'detect': True}


def test_implementation_smell_detector_detects_smells(module_mock, config_mock):
    detector = ConcreteImplementationSmellDetector()
    smells = detector.detect(module_mock, config_mock)
    assert len(smells) > 0


def test_implementation_smell_detector_no_smells(module_mock):
    detector = ConcreteImplementationSmellDetector()
    smells = detector.detect(module_mock, {'detect': False})
    assert len(smells) == 0


def test_design_smell_detector_detects_smells(module_mock, config_mock):
    detector = ConcreteDesignSmellDetector()
    smells = detector.detect(module_mock, config_mock)
    assert len(smells) > 0


def test_design_smell_detector_no_smells(module_mock):
    detector = ConcreteDesignSmellDetector()
    smells = detector.detect(module_mock, {'detect': False})
    assert len(smells) == 0


def test_smell_creation(module_mock):
    detector = ConcreteImplementationSmellDetector()
    smell = detector._create_smell(module_mock.name, module_mock, "Dummy smell", line=10)
    assert smell is not None
    assert smell['details'] == "Dummy smell"
    assert smell['location'] == "Line 10"


# def test_iterate_functions_and_methods_error_handling(module_mock, caplog):
#     module_mock.functions = None  # Mimic an AttributeError scenario
#     detector = ConcreteImplementationSmellDetector()
#
#     with caplog.at_level(logging.ERROR):
#         list(detector._iterate_functions_and_methods(module_mock))
#
#     # Print all captured log records for debugging
#     for record in caplog.records:
#         print(f"{record.levelname}: {record.message}")
#
#     # Assert that the expected error message is in the error logs
#     error_logs = [record.message for record in caplog.records if record.levelname == 'ERROR']
#     assert "Error iterating functions and methods" in error_logs, "Should log an error for invalid modules"
