import json

def get_config() -> dict:
    import os
    # get config.json_release path
    config_dir = os.path.abspath(__file__ + "/../")
    config_name = 'config.json'
    config_path = os.path.join(config_dir, config_name)

    with open(config_path, 'r') as f:
        config = json.load(f)

    return config

config = get_config()

