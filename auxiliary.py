import yaml

def parse_yaml(path_to_yaml):
    try:
        with open(path_to_yaml) as fp:
            yaml_data = yaml.safe_load(fp)
    except yaml.YAMLError as exc:
        print(exc)
        yaml_data = None
    return yaml_data
