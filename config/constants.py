import yaml
import os

PROJECT_ROOT = os.path.abspath(os.path.dirname((os.path.dirname(__file__))))


def get_config():
    config_filepath = os.path.join(PROJECT_ROOT, 'config', 'sensitive', 'development.yml')
    config = {}
    if os.path.exists(config_filepath):
        with open(config_filepath) as file:
            conf = yaml.load(file.read())
        for key in conf.keys():
            config[key] = conf.get(key)

    return config

__config = get_config()

DB = __config.get('database')

API_URL = "http://ip-api.com/json/"