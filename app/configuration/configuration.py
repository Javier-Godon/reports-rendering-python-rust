import yaml
from yaml import Loader

from definitions import CONFIG_PATH

yaml_file = open(CONFIG_PATH, 'r')
data = yaml.load(yaml_file, Loader=Loader)


def get_data():
    return data
