import json
import logging


def load_config(default_path='src/default_config.json', user_path=None):
    config = {}
    try:
        with open(default_path, 'r') as file:
            config = json.load(file)
    except FileNotFoundError:
        logging.error(f"Default configuration file not found at {default_path}.")
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
