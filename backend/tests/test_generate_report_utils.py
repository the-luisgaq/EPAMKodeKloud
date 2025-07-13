import pandas as pd
from app.utils.generate_report import convert_to_hours, merge_activity_data


def test_convert_to_hours():
    assert convert_to_hours("1 hour") == 1.0
    assert convert_to_hours("30 minutes") == 0.5
    assert convert_to_hours(2) == 2.0
    assert convert_to_hours(None) == 0.0


def test_merge_activity_data():
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
            "Lessons Completed": [1, 0],
            "Video Hours Watched": ["1 hour", "0"],
            "Labs Completed": [0, 0],
        }
    )
    result = merge_activity_data(admin_df, activity_df)
    assert list(result.columns) == [
        "Name",
        "Email",
        "Program",
        "Lessons Completed",
        "Video Hours Watched",
        "Labs Completed",
        "License Accepted",
        "Status",
    ]

    bob = result[result["Email"] == "bob@example.com"].iloc[0]
    assert bob["License Accepted"] == "X"
    assert bob["Status"] == "No activity or progress"

    alice = result[result["Email"] == "alice@example.com"].iloc[0]
    assert alice["License Accepted"] == "\u2713"
    assert alice["Status"] == ""
