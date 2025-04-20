import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_sheet(sheet_id, worksheet_name="kr"):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
    client = gspread.authorize(creds)
    return client.open_by_key(sheet_id).worksheet(worksheet_name)
