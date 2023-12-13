import json


def load_config(default_path='./default_config.json', user_path=None):
    with open(default_path, 'r') as file:
        config = json.load(file)

    if user_path:
        with open(user_path, 'r') as file:
            user_config = json.load(file)
            # Merge user config into the default config
            for smell, settings in user_config.get("Smells", {}).items():
                if smell in config["Smells"]:
                    config["Smells"][smell].update(settings)
                else:
                    config["Smells"][smell] = settings
    return config
