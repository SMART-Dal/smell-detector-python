# import pytest
# from unittest.mock import MagicMock
# from src.smells.architecture_smells.god_component import GodComponentDetector

# @pytest.fixture
# def detector():
#     return GodComponentDetector()

# @pytest.fixture
# def mock_package():
#     mock_package = MagicMock()
#     mock_package.modules = [
#         MagicMock(classes=[MagicMock(start_line=1, end_line=10) for _ in range(10)], name=f"Module_{i}") for i in range(3)
#     ]
#     return mock_package

# # Test case for package with total LOC and total number of classes below the thresholds
# def test_detect_god_component_below_threshold(detector, mock_package):
#     smells = detector.detect(mock_package, {})
#     assert len(smells) == 0

# # Test case for package with total LOC exceeding the threshold
# def test_detect_god_component_above_loc_threshold(detector, mock_package):
#     mock_package.modules.append(MagicMock(classes=[MagicMock(start_line=1, end_line=100) for _ in range(30)], name="Module_4"))
#     smells = detector.detect(mock_package, {})
#     assert len(smells) == 1
#     assert "LOC" in smells[0]["details"]

# # Test case for package with total number of classes exceeding the threshold
# def test_detect_god_component_above_num_classes_threshold(detector, mock_package):
#     mock_package.modules.append(MagicMock(classes=[MagicMock(start_line=1, end_line=10) for _ in range(31)], name="Module_4"))
#     smells = detector.detect(mock_package, {})
#     assert len(smells) == 1
#     assert "classes" in smells[0]["details"]

# # Test case for package with both total LOC and total number of classes exceeding the thresholds
# def test_detect_god_component_above_both_thresholds(detector, mock_package):
#     mock_package.modules.append(MagicMock(classes=[MagicMock(start_line=1, end_line=100) for _ in range(31)], name="Module_4"))
#     smells = detector.detect(mock_package, {})
#     assert len(smells) == 1
#     assert "LOC" in smells[0]["details"]
#     assert "classes" in smells[0]["details"]

import pytest
from unittest.mock import MagicMock
from src.smells.architecture_smells.god_component import GodComponentDetector

@pytest.fixture
def detector():
    return GodComponentDetector()

# Mock a module with total LOC and total number of classes below the thresholds
@pytest.fixture
def mock_module_below_threshold():
    mock_module = MagicMock()
    mock_module.classes = [MagicMock(start_line=1, end_line=100) for _ in range(10)]
    return mock_module

# Mock a module with total LOC exceeding the threshold
@pytest.fixture
def mock_module_above_loc_threshold():
    mock_module = MagicMock()
    mock_module.classes = [MagicMock(start_line=1, end_line=30001)]
    return mock_module

# Mock a module with total number of classes exceeding the threshold
@pytest.fixture
def mock_module_above_num_classes_threshold():
    mock_module = MagicMock()
    mock_module.classes = [MagicMock(start_line=1, end_line=100) for _ in range(31)]
    return mock_module

# Test case for package with total LOC and total number of classes below the thresholds
def test_detect_god_component_below_threshold(detector, mock_module_below_threshold):
    package_details = {"test_package": [mock_module_below_threshold]}
    smells = detector.detect(package_details, {})
    assert len(smells) == 0

# Test case for package with total LOC exceeding the threshold
def test_detect_god_component_above_loc_threshold(detector, mock_module_above_loc_threshold):
    package_details = {"test_package": [mock_module_above_loc_threshold]}
    smells = detector.detect(package_details, {})
    print(smells)
    assert len(smells) == 1
    assert "LOC" in smells[0]['details']

# Test case for package with total number of classes exceeding the threshold
def test_detect_god_component_above_num_classes_threshold(detector, mock_module_above_num_classes_threshold):
    package_details = {"test_package": [mock_module_above_num_classes_threshold]}
    smells = detector.detect(package_details, {})
    assert len(smells) == 1
    assert "classes" in smells[0]['details']

# Test case for package with both total LOC and total number of classes exceeding the thresholds
def test_detect_god_component_above_both_thresholds(detector, mock_module_above_loc_threshold, mock_module_above_num_classes_threshold):
    package_details = {"test_package": [mock_module_above_loc_threshold, mock_module_above_num_classes_threshold]}
    smells = detector.detect(package_details, {})
    assert len(smells) == 1
    assert "LOC" in smells[0]['details']
    assert "classes" in smells[0]['details']