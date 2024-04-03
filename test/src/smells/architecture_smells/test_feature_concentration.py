import pytest
from unittest.mock import MagicMock
from src.smells.architecture_smells.feature_concentration import FeatureComponentDetector

@pytest.fixture
def detector():
    return FeatureComponentDetector()

# Test case for no smell detected
def test_no_feature_concentration_smell(detector):
    # Mocking a package with modules having classes with external dependencies
    mock_package = MagicMock()
    mock_package.modules = [
        MagicMock(classes=[
            MagicMock(external_dependencies=["module1.py", "module2.py"]),
            MagicMock(external_dependencies=["module1.py", "module3.py"]),
            MagicMock(external_dependencies=["module2.py", "module3.py"])
        ])
    ]
    smells = detector.detect(mock_package, {})
    assert len(smells) == 0

# Test case for smell detected
def test_feature_concentration_smell(detector):
    # Mocking a package with modules having classes with external dependencies
    mock_package = MagicMock()
    mock_package.modules = [
        MagicMock(classes=[
            MagicMock(external_dependencies=["moduleB.py"]),
        ]),
        MagicMock(classes=[
            MagicMock(external_dependencies=["moduleA.py", "moduleB.py"]),
        ]),
        MagicMock(classes=[
            MagicMock(external_dependencies=["moduleA.py", "moduleB.py"]),
            MagicMock(external_dependencies=["moduleC.py"]),
        ]),
        MagicMock(classes=[
            MagicMock(external_dependencies=["moduleE.py"]),
        ]),
        MagicMock(classes=[
            MagicMock(external_dependencies=["moduleD.py"]),
        ])
    ]
    smells = detector.detect(mock_package, {})
    assert len(smells) == 1
