import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials

def init():
        # Connect to Google Sheets
        scope = ['https://www.googleapis.com/auth/spreadsheets',
                "https://www.googleapis.com/auth/drive"]

        credentials = ServiceAccountCredentials.from_json_keyfile_name(f"{os.getenv('DIR_PATH')}\\gsheet\\credentials.json", scope)
        client = gspread.authorize(credentials)
        return client

def create():
        client = init()
        sheet = client.create("wina_idx")
        sheet.share(os.getenv('GSHEET_ACC'), perm_type='user', role='writer')
        print('Sheet created.')
        return sheet

def open():
        client = init()
        sheet = client.open("wina_idx").sheet1
        print('Sheet opened.')
        return sheet

def get():
        sheet = open()
        print('Get all data from sheet.')
        return sheet.get_all_values()

def write(data):
        sheet = open()
        sheet.clear()
        for idx, item in enumerate(data):
                sheet.update(f"A{idx+1}:D{idx+1}", [[item[0], item[2], item[3], item[4]]])
        return print('Batch update done.')
