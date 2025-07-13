from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_report_download_error(monkeypatch):
    def raise_error(*args, **kwargs):
        raise Exception("boom")

    monkeypatch.setattr("app.routers.report.blob.download_blob_to_file", raise_error)

    response = client.post("/report")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to download blob"


def test_get_report_data_download_error(monkeypatch):
    def raise_error(*args, **kwargs):
        raise Exception("boom")

    monkeypatch.setattr("app.routers.report.blob.download_blob_to_file", raise_error)

    response = client.get("/report/data")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to download blob"
