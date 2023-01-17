import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

def call():
        # Connect to Google Sheets
        scope = ['https://www.googleapis.com/auth/spreadsheets',
                "https://www.googleapis.com/auth/drive"]

        credentials = ServiceAccountCredentials.from_json_keyfile_name(f"{os.getenv('DIR_PATH')}\\gsheet\\credentials.json", scope)
        client = gspread.authorize(credentials)

        # Initiate sheet
        # sheet = client.create("open_low_result")
        # sheet.share('gammarinaldi@gmail.com', perm_type='user', role='writer')

        # Open the spreadsheet
        sheet = client.open("open_low_result").sheet1

        return sheet.get_all_values()