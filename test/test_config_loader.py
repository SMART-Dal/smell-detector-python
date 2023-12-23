# test_config_loader.py

import json
import pytest
from unittest.mock import mock_open, patch

from src.config_loader import load_config

# Sample data for default and user configurations
default_config_data = {
    "Smells": {
        "LongMethod": {"enable": True, "threshold": 20}
    }
}

user_config_data = {
    "Smells": {
        "LongMethod": {"threshold": 10}  # Override the default threshold
    }
}


def test_load_default_config():
    """Test loading the default configuration without a user path."""
    with patch("builtins.open", mock_open(read_data=json.dumps(default_config_data))) as mock_file:
        config = load_config()
        mock_file.assert_called_with('src/default_config.json', 'r')
        assert config == default_config_data, "The default configuration should be loaded correctly."


def test_load_user_config():
    """Test loading and merging the user configuration with the default."""
    mock_file = mock_open()
    mock_file.side_effect = [
        mock_open(read_data=json.dumps(default_config_data)).return_value,  # First call to open (default config)
        mock_open(read_data=json.dumps(user_config_data)).return_value  # Second call to open (user config)
    ]
    with patch("builtins.open", mock_file) as mock_open_function:
        config = load_config(user_path='path/to/user_config.json')
        assert mock_open_function.call_args_list[0] == patch.call('src/default_config.json', 'r'), "Should open default config"
        assert mock_open_function.call_args_list[1] == patch.call('path/to/user_config.json', 'r'), "Should open user config"
        assert config["Smells"]["LongMethod"]["threshold"] == 10, "The user configuration should override the default."


def test_load_config_with_missing_default():
    """Test behavior when the default configuration file is missing."""
    with pytest.raises(FileNotFoundError):
        load_config(default_path='nonexistent/path.json')


def test_load_config_with_malformed_default():
    """Test behavior when the default configuration file is malformed."""
    with patch("builtins.open", mock_open(read_data="not JSON")):
        with pytest.raises(json.JSONDecodeError):
            load_config()


def test_load_config_with_missing_user_config():
    """Test behavior when the user configuration file is missing."""
    with patch("builtins.open", mock_open(read_data=json.dumps(default_config_data))) as mock_default:
        with pytest.raises(FileNotFoundError):
            load_config(default_path='src/default_config.json', user_path='nonexistent/path.json')
        mock_default.assert_called_with('src/default_config.json', 'r')



def test_load_config_with_malformed_user_config():
    """Test behavior when the user configuration file is malformed."""
    with patch("builtins.open", mock_open(read_data=json.dumps(default_config_data))) as mock_default:
        with patch("builtins.open", mock_open(read_data="not JSON")):
            with pytest.raises(json.JSONDecodeError):
                load_config(user_path='path/to/malformed_user_config.json')

# Add more tests as necessary for different scenarios and edge cases.
