import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

def load_sheet(sheet_id=None, worksheet_name=None):
    """
    Load Google Sheet using service account credentials.
    
    Args:
        sheet_id (str, optional): Google Sheet ID. If None, uses default sheet.
        worksheet_name (str, optional): Worksheet name. If None, returns the sheet object.
    
    Returns:
        gspread.Worksheet or gspread.Spreadsheet: The worksheet or spreadsheet object.
    """
    try:
        # Define the scope
        scope = ['https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive']

        # Get absolute path to credentials file
        current_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        creds_path = os.path.join(current_dir, 'creds.json')

        # Load credentials from service account file
        credentials = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)

        # Authorize the client
        client = gspread.authorize(credentials)

        # Get the spreadsheet
        if sheet_id:
            sheet = client.open_by_key(sheet_id)
        else:
            sheet = client.open("Stock News")

        # Return worksheet if name is provided
        if worksheet_name:
            return sheet.worksheet(worksheet_name)
        return sheet

    except Exception as e:
        print(f"Error loading sheet: {str(e)}")
        return None 