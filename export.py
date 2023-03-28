import os.path
import logging
import json
from googleapiclient.discovery import build
from google.oauth2 import service_account
from googleapiclient.errors import HttpError

json_creds = json.loads(os.environ.get('CREDENTIALS'))
with open('/tmp/credentials.json', 'w') as creds:
    creds.write(json.dumps(json_creds, indent=4))

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SERVICE_ACCOUNT_FILE = '/tmp/credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

def export_data(spreadsheet_id, range_name):
    try:
        service = build('sheets', 'v4', credentials=credentials)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                            range=range_name).execute()
        values = result.get('values', [])        
        return values
    
    except HttpError as err:
         logging.error(err)