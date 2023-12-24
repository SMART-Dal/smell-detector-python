import pytest
from src.sourcemodel.sm_package import SMPackage


@pytest.fixture
def package():
    return SMPackage(name="TestPackage")


@pytest.fixture
def module_mock(mocker):
    # Creating a mock module with a mock analyze method
    module = mocker.MagicMock()
    module.analyze = mocker.MagicMock()
    return module


def test_smpackage_initialization(package):
    assert package.name == "TestPackage", "The name should be initialized correctly"
    assert len(package.modules) == 0, "Initially, there should be no modules"


def test_add_module(package, module_mock):
    package.add_module(module_mock)
    assert module_mock in package.modules, "The module should be added to the package"


def test_analyze(package, module_mock):
    package.add_module(module_mock)
    package.analyze()
    module_mock.analyze.assert_called_once_with(), "The analyze method of each module should be called"
