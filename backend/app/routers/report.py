import tempfile
import os
import json
from fastapi import APIRouter, HTTPException
from ..utils.generate_report import generate_report
from ..external_services import blob

router = APIRouter(prefix="/report", tags=["report"])


@router.post("/")
async def create_report():
    with tempfile.TemporaryDirectory() as tmpdir:
        admin_path = os.path.join(tmpdir, "admin.xlsx")
        activity_path = os.path.join(tmpdir, "activity.xlsx")
        output_excel_path = os.path.join(tmpdir, "kodekloud_report.xlsx")
        output_json_path = os.path.join(tmpdir, "kodekloud_data.json")

        try:
            blob.download_blob_to_file(
                "cloudkit-inputs",
                "kode_kloud/root/KodeKloud2025Admin.xlsx",
                admin_path,
            )
            blob.download_blob_to_file(
                "cloudkit-inputs",
                "kode_kloud/root/activity_leaderboard.xlsx",
                activity_path,
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail="Failed to download blob") from exc

        data = generate_report(admin_path, activity_path, output_excel_path, output_json_path)

    return data


@router.get("/data")
async def get_report_data():
    """Return the latest generated JSON report from Blob Storage."""
    with tempfile.TemporaryDirectory() as tmpdir:
        json_path = os.path.join(tmpdir, "kodekloud_data.json")
        try:
            blob.download_blob_to_file(
                "cloudkit-inputs",
                "kode_kloud/root/kodekloud_data.json",
                json_path,
            )
        except Exception as exc:
            raise HTTPException(status_code=500, detail="Failed to download blob") from exc
        with open(json_path, "r") as f:
            return json.load(f)
