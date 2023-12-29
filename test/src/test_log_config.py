import logging
import os
import tempfile
import time

import pytest

from src.log_config import ensure_log_directory_exists, setup_logging


@pytest.fixture
def log_directory():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname
        # Attempt cleanup
        for _ in range(3):  # retry logic
            try:
                logging.shutdown()
                os.unlink(tmpdirname)
                break
            except PermissionError:
                time.sleep(1)  # wait for file to be released
            except Exception as e:
                print(f"Cleanup failed: {e}")
                break


@pytest.fixture
def mock_os_path_exists(mocker):
    return mocker.patch('os.path.exists', return_value=True)


@pytest.fixture
def mock_os_makedirs(mocker):
    return mocker.patch('os.makedirs')


@pytest.fixture
def mock_rotating_file_handler(mocker):
    return mocker.patch('logging.handlers.RotatingFileHandler')


def test_ensure_log_directory_exists_success(log_directory, mock_os_path_exists, mock_os_makedirs):
    # Test if the log directory is correctly ensured to exist
    assert ensure_log_directory_exists(log_directory) == log_directory, "Should return the log directory path"


def test_ensure_log_directory_creation_failure(mocker, log_directory, mock_os_makedirs):
    # Simulate a scenario where creating a directory raises an exception
    mock_os_makedirs.side_effect = Exception("Creation failed")
    assert ensure_log_directory_exists(log_directory) is None, "Should handle the directory creation exception"


def test_setup_logging_file_handler(mocker, log_directory, mock_os_path_exists, mock_rotating_file_handler,
                                    mock_os_makedirs):
    # Test if the RotatingFileHandler is added to the logger
    mock_add_handler = mocker.patch.object(logging.getLogger(), 'addHandler')
    setup_logging(log_directory)
    assert mock_add_handler.called, "Should add file handler to logger"


# Include a teardown method to handle any cleanup
@pytest.fixture(autouse=True)
def cleanup():
    yield
    logging.shutdown()  # This will close all handlers.
