import pandas as pd
import json
import re
import warnings
from openpyxl import load_workbook
from openpyxl.styles import PatternFill
from ..external_services import blob

warnings.simplefilter("ignore")


def convert_to_hours(value):
    if pd.isna(value):
        return 0.0
    if isinstance(value, (int, float)):
        return float(value)
    value = str(value).strip().lower()
    if 'hour' in value:
        num = re.findall(r"[\d\.]+", value)
        return float(num[0]) if num else 0.0
    elif 'minute' in value:
        num = re.findall(r"[\d\.]+", value)
        return float(num[0]) / 60 if num else 0.0
    return 0.0


def generate_report(admin_path, activity_path, output_excel_path, output_json_path):
    admin_df = pd.read_excel(admin_path)
    activity_df = pd.read_excel(activity_path)

    admin_df['Email'] = admin_df['Email'].str.strip().str.lower()
    activity_df['Email'] = activity_df['Email'].str.strip().str.lower()

    admin_df = admin_df[['Name', 'Email', 'Program', 'License Accepted']]
    activity_df = activity_df[['Email', 'Lessons Completed', 'Video Hours Watched', 'Labs Completed']]

    admin_df = admin_df[admin_df['Program'].str.strip().str.upper() != 'LPC']

    merged = pd.merge(admin_df, activity_df, on='Email', how='left')

    merged['Lessons Completed'] = merged['Lessons Completed'].fillna(0).astype(int)
    merged['Video Hours Watched'] = merged['Video Hours Watched'].apply(convert_to_hours)
    merged['Labs Completed'] = merged['Labs Completed'].fillna(0).astype(int)

    def activity_status(row):
        if row['Lessons Completed'] == 0 and row['Video Hours Watched'] == 0 and row['Labs Completed'] == 0:
            return 'No activity or progress'
        return ''

    merged['Status'] = merged.apply(activity_status, axis=1)

    def license_display(val):
        if isinstance(val, str) and val.strip().lower() == 'no':
            return 'X'
        return '✓'

    merged['License Accepted Display'] = merged['License Accepted'].apply(license_display)

    final_columns = ['Name', 'Email', 'Program', 'Lessons Completed', 'Video Hours Watched', 'Labs Completed', 'License Accepted Display', 'Status']
    display_df = merged[final_columns].rename(columns={"License Accepted Display": "License Accepted"})
    display_df.to_excel(output_excel_path, index=False)

    wb = load_workbook(output_excel_path)
    ws = wb.active

    red_fill = PatternFill(start_color='FFC7CE', end_color='FFC7CE', fill_type='solid')
    orange_fill = PatternFill(start_color='FFD580', end_color='FFD580', fill_type='solid')

    for row in ws.iter_rows(min_row=2):
        status = row[7].value
        license_col = row[6].value
        if status == 'No activity or progress':
            for cell in row:
                cell.fill = red_fill
        elif license_col == 'X':
            for cell in row:
                cell.fill = orange_fill

    wb.save(output_excel_path)

    json_data = display_df.to_dict(orient='records')
    with open(output_json_path, 'w') as f:
        json.dump(json_data, f, indent=2)

    blob.upload_file_to_blob(
        "cloudkit-inputs",
        output_json_path.split('/')[-1],
        output_json_path,
    )
    return json_data
