import os
import logging
from azure.storage.blob import BlobServiceClient

# Configuration loaded from GitHub Secrets or the environment
STORAGE_CONNECTION_STRING = os.getenv("STORAGE_CONNECTION_STRING")
CONTAINER_SOURCE = os.getenv("CONTAINER_SOURCE", "cloudkit-inputs")
CONTAINER_INPUTS = os.getenv("CONTAINER_INPUTS", "cloudkit-inputs")
INPUT_FOLDER = os.getenv("INPUT_FOLDER", "kode_kloud/input")
ARCHIVE_FOLDER = os.getenv("ARCHIVE_FOLDER", "kode_kloud/input/archive")

blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)

def run_my_logic():
    logging.info("Checking required files in the source container...")

    source_container = blob_service_client.get_container_client(CONTAINER_SOURCE)
    input_container = blob_service_client.get_container_client(CONTAINER_INPUTS)
    required_files = {"activity_leaderboard.xlsx", "KodeKloud2025Admin.xlsx"}

    # Verify that the required files are present
    source_blobs = list(source_container.list_blobs())
    found_files = {blob.name for blob in source_blobs if blob.name in required_files}

    if not required_files.issubset(found_files):
        logging.info("Required files are not available yet.")
        return

    logging.info("Moving existing files in the input container to /archive...")

    for blob in input_container.list_blobs(name_starts_with=f"{INPUT_FOLDER}/"):
        if blob.name.endswith(".xlsx") or blob.name.endswith(".json"):
            src = input_container.get_blob_client(blob.name)
            dst = input_container.get_blob_client(f"{ARCHIVE_FOLDER}/{blob.name}")
            dst.start_copy_from_url(src.url)
            src.delete_blob()

    logging.info("Moving new files to the input container...")

    for filename in required_files:
        src = source_container.get_blob_client(filename)
        dst = input_container.get_blob_client(f"{INPUT_FOLDER}/{filename}")
        dst.start_copy_from_url(src.url)
        src.delete_blob()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    run_my_logic()
