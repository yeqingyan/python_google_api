# Note: I used my google accout to create the client_secret.json, you can change it to yours, it need to enable the Google Driver and Sheets APIs.

from __future__ import print_function
import httplib2
import os
import json
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# Check python version
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None


# Get data from json file
def get_json_data():
    INPUT_FILE = "example.json"
    headers = set()

    input = json.load(open(INPUT_FILE))
    for row in input:
        for item in input[row]:
            headers.add(item)
    headers = list(headers)
    data = [[""] + headers]

    for row in input:
        output_row = [row]
        for item in headers:
            if item in input[row]:
                output_row.append("1")
            else:
                output_row.append("0")
        data.append(output_row)

    return data


# Create credential files
def get_credentials():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    CLIENT_SECRET_FILE = 'client_secret.json'
    APPLICATION_NAME = 'Google Sheets API Python Quickstart'

    credential_dir = os.path.join("./", '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,'track_revenue.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


# Write to spread sheet
def write_to_spreadsheet(sheet_content):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?version=v4')
    driver_service = discovery.build('drive', 'v3', http=http)
    sheets_service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    # Create a new spread sheet
    result = sheets_service.spreadsheets().create(body={"properties": {"title": "example"}}).execute()
    sheet_id = result.get('spreadsheetId')
    spreadsheet_url = result.get('spreadsheetUrl')
    # Let anyone can read the sheet
    driver_service.permissions().create(fileId=sheet_id,body={"role": "reader", "type":"anyone"}).execute()
    # Write to sheet
    result = sheets_service.spreadsheets().values().update(spreadsheetId=sheet_id, range='A1:Z100', valueInputOption='RAW', body={'values': sheet_content}).execute()
    print("Sheet url is: " + spreadsheet_url)
    return

if __name__ == '__main__':
    write_to_spreadsheet(get_json_data())