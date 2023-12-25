import logging
import os
import pytest

from src.export.exporter import export_to_json, export_to_csv

# Sample data for testing
sample_data = [{
    "package": "input_package",
    "module_name": "test_module.py",
    "class_name": "TestClass",
    "loc": 13,
    "wmc": 3,
    "nom": 3,
    "nopm": 2,
    "nof": 0,
    "nopf": 0,
    "lcom": 2,
    "fan_in": 3,
    "fan_out": 4
}
]

# Test directory and file names
test_output_dir = "test_output"
test_file_name = "test"


@pytest.fixture
def mock_open(mocker):
    return mocker.patch("builtins.open", mocker.mock_open())


@pytest.fixture
def mock_json_dump(mocker):
    return mocker.patch("json.dump")


@pytest.fixture
def mock_csv_writer(mocker):
    return mocker.patch("csv.DictWriter")


@pytest.fixture
def mock_logging(mocker):
    mocker.patch("logging.info")
    mocker.patch("logging.error")


@pytest.fixture
def create_test_output_dir():
    if not os.path.exists(test_output_dir):
        os.makedirs(test_output_dir)
    yield
    os.rmdir(test_output_dir)


# Test successful JSON export
def test_export_to_json_success(mock_open, mock_json_dump, mock_logging, create_test_output_dir):
    expected_path = os.path.join(test_output_dir, f"{test_file_name}.json")
    export_to_json(sample_data, test_output_dir, test_file_name)
    mock_json_dump.assert_called_once()
    logging.info.assert_called_with(f"JSON data successfully exported to {expected_path}")


# Test successful CSV export
def test_export_to_csv_success(mock_open, mock_csv_writer, mock_logging, create_test_output_dir):
    expected_path = os.path.join(test_output_dir, f"{test_file_name}.csv")
    export_to_csv(sample_data, test_output_dir, test_file_name)
    mock_csv_writer.assert_called_once()
    logging.info.assert_called_with(f"CSV data successfully exported to {expected_path}")


# Test handling of empty data for CSV
def test_export_to_csv_no_data(mock_logging):
    export_to_csv([], test_output_dir, test_file_name)
    logging.error.assert_called_once_with(f"No data provided to export for {test_file_name}.csv")


# Test IOError handling for JSON
def test_export_to_json_io_error(mock_open, mock_logging, create_test_output_dir):
    expected_path = os.path.join(test_output_dir, f"{test_file_name}.json")
    mock_open.side_effect = IOError("Test IOError")
    export_to_json(sample_data, test_output_dir, test_file_name)
    logging.error.assert_called_with(
        f"IOError while writing JSON to {expected_path}: Test IOError")


# Test IOError handling for CSV
def test_export_to_csv_io_error(mock_open, mock_logging, create_test_output_dir):
    expected_path = os.path.join(test_output_dir, f"{test_file_name}.csv")
    mock_open.side_effect = IOError("Test IOError")
    export_to_csv(sample_data, test_output_dir, test_file_name)
    logging.error.assert_called_with(
        f"IOError while writing CSV to {expected_path}: Test IOError")


# Test unexpected error handling for JSON
def test_export_to_json_unexpected_error(mock_open, mock_logging, create_test_output_dir):
    expected_path = os.path.join(test_output_dir, f"{test_file_name}.json")
    mock_open.side_effect = Exception("Unexpected Error")
    export_to_json(sample_data, test_output_dir, test_file_name)
    logging.error.assert_called_with(
        f"Unexpected error while writing JSON to {expected_path}: Unexpected Error")


# Test unexpected error handling for CSV
def test_export_to_csv_unexpected_error(mock_open, mock_logging, create_test_output_dir):
    expected_path = os.path.join(test_output_dir, f"{test_file_name}.csv")
    mock_open.side_effect = Exception("Unexpected Error")
    export_to_csv(sample_data, test_output_dir, test_file_name)
    logging.error.assert_called_with(
        f"Unexpected error while writing CSV to {expected_path}: Unexpected Error")
