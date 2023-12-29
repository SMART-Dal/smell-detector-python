import json
import logging
import os

script_dir = os.path.dirname(os.path.abspath(__file__))
DEFAULT_CONFIG_PATH = os.path.join(script_dir, 'smells', 'default_config.json')


def load_config(user_path=None):
    config = {}
    try:
        with open(DEFAULT_CONFIG_PATH, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        logging.error(f"Default configuration file not found at {DEFAULT_CONFIG_PATH}.")
        raise
    except json.JSONDecodeError as e:
        logging.error(f"Invalid JSON in the default configuration: {e}")
        raise
    except Exception as e:
        logging.error(f"An unexpected error occurred while loading the default configuration: {e}")
        raise

    if user_path:
        try:
            with open(user_path, 'r') as file:
                user_config = json.load(file)
                # Merge user config into the default config
                for smell, settings in user_config.get("Smells", {}).items():
                    if smell in config["Smells"]:
                        config["Smells"][smell].update(settings)
                    else:
                        config["Smells"][smell] = settings
        except FileNotFoundError:
            logging.warning(f"User configuration file not found at {user_path}. Continuing with default settings.")
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON in the user configuration: {e}")
            raise
        except Exception as e:
            logging.error(f"An unexpected error occurred while loading the user configuration: {e}")
            raise

    return config
