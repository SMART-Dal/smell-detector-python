import json
import pytest

from src.config_loader import load_config

# Sample content for default and user configurations
default_config_content = {
    "Smells": {
        "LongMethod": {
            "enable": True,
            "threshold": 20
        }
        # ... add other default settings as needed
    }
}

user_config_content = {
    "Smells": {
        "LongMethod": {
            "enable": False,
            "threshold": 15
        }
        # ... add other user settings as needed
    }
}


@pytest.fixture
def mock_open_default(mocker):
    # Mocking open for default configuration
    return mocker.mock_open(read_data=json.dumps(default_config_content))


@pytest.fixture
def mock_open_user(mocker):
    # Mocking open for user configuration
    return mocker.mock_open(read_data=json.dumps(user_config_content))


def test_load_default_config_success(mocker, mock_open_default):
    mocker.patch('builtins.open', mock_open_default)
    mocker.patch('json.load', return_value=default_config_content)

    config = load_config()
    assert config == default_config_content, "Should load the default configuration"


def test_load_default_config_file_not_found(mocker):
    mocker.patch('builtins.open', side_effect=FileNotFoundError)

    with pytest.raises(FileNotFoundError):
        load_config()


def test_load_user_config_overrides_default(mocker, mock_open_default, mock_open_user):
    mocker.patch('builtins.open', mock_open_default)
    mocker.patch('json.load', side_effect=[default_config_content, user_config_content])

    config = load_config(user_path='path/to/user_config.json')
    assert config['Smells']['LongMethod']['enable'] == False, "User configuration should override default"
    assert config['Smells']['LongMethod']['threshold'] == 15, "User configuration should override default"


def test_load_config_with_invalid_json(mocker, mock_open_default):
    mocker.patch('builtins.open', mock_open_default)
    mocker.patch('json.load', side_effect=json.JSONDecodeError("Expecting value", "doc", 0))

    with pytest.raises(json.JSONDecodeError):
        load_config()
