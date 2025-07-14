from fastapi.testclient import TestClient
from main import app
import pandas as pd
import json
import shutil

client = TestClient(app)


def test_create_report_download_error(monkeypatch):
    def raise_error(*args, **kwargs):
        raise Exception("boom")

    monkeypatch.setattr("app.routers.kodekloud_report.storage.download_blob_to_file", raise_error)

    response = client.post("/report")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to download blob"


def test_get_report_data_download_error(monkeypatch):
    def raise_error(*args, **kwargs):
        raise Exception("boom")

    monkeypatch.setattr("app.routers.kodekloud_report.storage.download_blob_to_file", raise_error)

    response = client.get("/report/data")
    assert response.status_code == 500
    assert response.json()["detail"] == "Failed to download blob"


def test_create_report_success(monkeypatch, tmp_path):
    admin_df = pd.DataFrame(
        {
            "Name": ["Alice", "Bob"],
            "Email": ["alice@example.com", "bob@example.com"],
            "Program": ["Bootcamp", "Bootcamp"],
            "License Accepted": ["Yes", "No"],
        }
    )
    activity_df = pd.DataFrame(
        {
            "Email": ["alice@example.com", "bob@example.com"],
            "Lessons Completed": [2, 0],
            "Video Hours Watched": ["1 hour", 0],
            "Labs Completed": [3, 0],
        }
    )
    admin_src = tmp_path / "admin.xlsx"
    activity_src = tmp_path / "activity.xlsx"
    admin_df.to_excel(admin_src, index=False)
    activity_df.to_excel(activity_src, index=False)

    def fake_download(container, blob_name, local_path):
        if "Admin" in blob_name:
            shutil.copy(admin_src, local_path)
        else:
            shutil.copy(activity_src, local_path)

    monkeypatch.setattr("app.routers.kodekloud_report.storage.download_blob_to_file", fake_download)
    monkeypatch.setattr("app.utils.kodekloud_generate_report.storage.download_blob_to_file", fake_download)
    monkeypatch.setattr("app.utils.kodekloud_generate_report.storage.upload_file_to_blob", lambda *a, **k: None)

    response = client.post("/report")
    assert response.status_code == 200
    expected = [
        {
            "Name": "Alice",
            "Email": "alice@example.com",
            "Program": "Bootcamp",
            "Lessons Completed": 2,
            "Video Hours Watched": 1.0,
            "Labs Completed": 3,
            "License Accepted": "\u2713",
            "Status": "",
        },
        {
            "Name": "Bob",
            "Email": "bob@example.com",
            "Program": "Bootcamp",
            "Lessons Completed": 0,
            "Video Hours Watched": 0.0,
            "Labs Completed": 0,
            "License Accepted": "X",
            "Status": "No activity or progress",
        },
    ]
    assert response.json() == expected


def test_get_report_data_success(monkeypatch, tmp_path):
    data = [{"foo": "bar"}]
    json_file = tmp_path / "kodekloud_data.json"
    with open(json_file, "w") as f:
        json.dump(data, f)

    def fake_download(container, blob_name, local_path):
        shutil.copy(json_file, local_path)

    monkeypatch.setattr("app.routers.kodekloud_report.storage.download_blob_to_file", fake_download)

    response = client.get("/report/data")
    assert response.status_code == 200
    assert response.json() == data
