import os
import glob
from google.cloud import storage

def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the given GCS bucket."""
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)
    print(f"Uploaded: {source_file_name} → gs://{bucket_name}/{destination_blob_name}")

def upload_fec_files_to_gcs(config):
    """Uploads FEC files (those without 'columns' key) to Google Cloud Storage."""
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = config['gcs']['credentials_file']
    bucket_name = config['gcs']['bucket']
    upload_folder = config['gcs']['upload_folder']

    for file_info in config['fec_data_files']:
        # Skip MySQL-bound files (those with 'columns')
        if 'columns' in file_info:
            continue

        # Expand wildcard patterns (e.g., *.txt)
        file_pattern = file_info['file']
        matched_files = glob.glob(file_pattern)

        if not matched_files:
            print(f"No files matched: {file_pattern}")
            continue

        for source_file in matched_files:
            filename = os.path.basename(source_file)
            destination_blob_name = f"{upload_folder}/{file_info['gcs_folder']}/{filename}"

            try:
                upload_blob(bucket_name, source_file, destination_blob_name)
            except Exception as e:
                print(f"Failed to upload {source_file}: {e}")
