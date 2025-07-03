import yaml
from pprint import pprint

from src.filessio_uploader import upload_fec_files_to_mysql
from src.gcs_uploader import upload_fec_files_to_gcs


if __name__ == "__main__":

    file_name = "config/config.yaml"
    
    with open(file_name, "r") as file:
        try:
            config = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            print(f"Error in configuration file: {exc}")
            exit(1)

    try:
        upload_fec_files_to_mysql(config)
        upload_fec_files_to_gcs(config)
    except Exception as e:
        print(f"An error occurred while uploading files to MySQL and GCS bucket: {e}")
        exit(1)

    