from datetime import datetime
from azure.storage.blob import BlobServiceClient
from ..core import settings


def get_blob_service_client():
    connection_string = settings.AZURE_STORAGE_CONNECTION_STRING
    if not connection_string:
        raise Exception("Missing AZURE_STORAGE_CONNECTION_STRING environment variable")
    return BlobServiceClient.from_connection_string(connection_string)


def download_blob_to_file(container_name: str, blob_name: str, local_path: str) -> None:
    blob_service_client = get_blob_service_client()
    blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
    with open(local_path, "wb") as file:
        download_stream = blob_client.download_blob()
        file.write(download_stream.readall())


def upload_file_to_blob(container_name: str, blob_name: str, local_path: str) -> None:
    blob_service_client = get_blob_service_client()
    container_client = blob_service_client.get_container_client(container_name)
    blob_client = container_client.get_blob_client(blob_name)

    if blob_client.exists():
        timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
        backup_blob_name = f"{blob_name.replace('.json', '')}_{timestamp}.json"
        backup_blob_client = container_client.get_blob_client(backup_blob_name)
        source_url = blob_client.url
        backup_blob_client.start_copy_from_url(source_url)

        all_blobs = sorted(
            [b for b in container_client.list_blobs(name_starts_with=blob_name.replace('.json', '')) if b.name.endswith('.json')],
            key=lambda b: b.last_modified,
            reverse=True
        )
        for old_blob in all_blobs[5:]:
            container_client.delete_blob(old_blob.name)

    with open(local_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
