import yaml
from pprint import pprint

from src.filessio_uploader import need_to_name  










if __name__ == "__main__":

    file_name = "config/config.yaml"
    
    with open(file_name, "r") as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(f"Error in configuration file: {exc}")
            exit(1)
    
    # Transform and Uploads data from a CSV file to the specified MySQL table.
    host = config['mysql']['host']
    port = config['mysql']['port']
    username = config['mysql']['username']
    password = config['mysql']['password']
    database = config['mysql']['database']

    # pprint(config)

    need_to_name(config)

