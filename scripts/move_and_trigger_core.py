import os
import logging
import requests
from azure.storage.blob import BlobServiceClient

# Config desde GitHub Secrets o entorno
STORAGE_CONNECTION_STRING = os.getenv("STORAGE_CONNECTION_STRING")
CONTAINER_SOURCE = os.getenv("CONTAINER_SOURCE", "kodekloudfiles")
CONTAINER_INPUTS = os.getenv("CONTAINER_INPUTS", "cloudkit-inputs")
INPUT_FOLDER = os.getenv("INPUT_FOLDER", "input")
ARCHIVE_FOLDER = os.getenv("ARCHIVE_FOLDER", "archive")
TRIGGER_URL = os.getenv("TRIGGER_URL")

blob_service_client = BlobServiceClient.from_connection_string(STORAGE_CONNECTION_STRING)

def run_my_logic():
    logging.info("Verificando archivos requeridos en el contenedor fuente...")

    source_container = blob_service_client.get_container_client(CONTAINER_SOURCE)
    input_container = blob_service_client.get_container_client(CONTAINER_INPUTS)
    required_files = {"activity_leaderboard.xlsx", "KodeKloud2025Admin.xlsx"}

    # Validar si los archivos requeridos están presentes
    source_blobs = list(source_container.list_blobs())
    found_files = {blob.name for blob in source_blobs if blob.name in required_files}

    if not required_files.issubset(found_files):
        logging.info("Archivos requeridos aún no están presentes.")
        return

    logging.info("Moviendo archivos existentes en el contenedor de entrada a /archive...")

    for blob in input_container.list_blobs(name_starts_with=f"{INPUT_FOLDER}/"):
        if blob.name.endswith(".xlsx") or blob.name.endswith(".json"):
            src = input_container.get_blob_client(blob.name)
            dst = input_container.get_blob_client(f"{ARCHIVE_FOLDER}/{blob.name}")
            dst.start_copy_from_url(src.url)
            src.delete_blob()

    logging.info("Moviendo archivos nuevos al contenedor de entrada...")

    for filename in required_files:
        src = source_container.get_blob_client(filename)
        dst = input_container.get_blob_client(f"{INPUT_FOLDER}/{filename}")
        dst.start_copy_from_url(src.url)
        src.delete_blob()

    logging.info("Llamando a la Azure Function para generar el reporte...")
    resp = requests.post(TRIGGER_URL)
    logging.info(f"Respuesta: {resp.status_code} - {resp.text}")
