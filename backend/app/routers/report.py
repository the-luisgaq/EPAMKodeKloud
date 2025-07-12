import tempfile
import os
import json
from fastapi import APIRouter
from ..utils import generate_report
from ..external_services import blob

router = APIRouter(prefix="/report", tags=["report"])


@router.post("/")
def create_report():
    with tempfile.TemporaryDirectory() as tmpdir:
        admin_path = os.path.join(tmpdir, "admin.xlsx")
        activity_path = os.path.join(tmpdir, "activity.xlsx")
        output_excel_path = os.path.join(tmpdir, "kodekloud_report.xlsx")
        output_json_path = os.path.join(tmpdir, "kodekloud_data.json")

        blob.download_blob_to_file(
            "cloudkit-inputs",
            "KodeKloud2025Admin.xlsx",
            admin_path,
        )
        blob.download_blob_to_file(
            "cloudkit-inputs",
            "activity_leaderboard.xlsx",
            activity_path,
        )

        data = generate_report.generate_report(admin_path, activity_path, output_excel_path, output_json_path)

    return data
