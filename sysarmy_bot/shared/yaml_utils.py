import yaml


def yaml_as_dict(yaml_file: str) -> dict:
    with open(yaml_file, 'r') as config_file:
        return yaml.safe_load(config_file)
