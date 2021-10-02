from __future__ import print_function
from flask import Flask , render_template

from ntpath import join
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import pandas as pd

from google.oauth2 import service_account

app = Flask(__name__)
SERVICE_ACCOUNT_FILE = 'keys.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)





# If modifying these scopes, delete the file token.json.


# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1MCPexSAlrZKtyvbiO-l9Of9QKAJVkKF9JevJZkBQIJg'





service = build('sheets', 'v4', credentials=creds)

# Call the Sheets API
sheet = service.spreadsheets()
result = sheet.values().get(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range="Database!C5:L11").execute()


values = result.get('values', [])


df = pd.DataFrame(values,columns=['Board','Tasks','Status','Priority','Responsible Person','Start Date','Finish Date' ,'Due Date' ,'Work Progress','Average Working hrs'])

print(df)
@app.route('/')

def progress():
    if not values:
        print('No data found.')
    else:
        members = []
        progress = []
        final_progress  = []
        for r in range(len(values)):
            if len(values[r]) == 9:
                members.append(values[r][4])
                progress.append(values[r][8])
        for i in progress:
            final_progress.append(float(i[0:len(i)-1]))
        return render_template('progress.html' , final_progress = final_progress , members = members)



@app.route('/tasks')
def task():
    x = df['Tasks']
    l = list(x)
    
    progress = df['Work Progress']
    p = []
    for i in progress:
        p.append(float(i[0:len(i)-1]))
    rp = df['Responsible Person']
    r = list(rp)
    hrs = list(df['Average Working hrs'])
    for i in range(len(hrs)):
        hrs[i] = float(hrs[i])

    return render_template('task.html',p=p,r = r, l = l,hrs= hrs)

if __name__ == "__main__":
    app.run(debug=True)
