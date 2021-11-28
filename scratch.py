import gspread
import time
import pprint
import calendar
from datetime import datetime


# <editor-fold desc="gs auth">
gs_name = 'scouting gamification'
path_to_gspread_credentials_json = '/Users/ysenkiv/Code/access files/personal/google sheets and drive for gspread/credentials.json'
path_to_gspread_authorized_user = '/Users/ysenkiv/Code/access files/personal/google sheets and drive for gspread/authorized_user.json'
google_client = gspread.oauth(credentials_filename=path_to_gspread_credentials_json, authorized_user_filename=path_to_gspread_authorized_user)
gs = google_client.open(gs_name)
log_sheet = gs.worksheet('log')
db_sheet = gs.worksheet('db')
assessment_sheet = gs.worksheet('team')
# </editor-fold>

test_data = assessment_sheet.batch_get(('A1:A2',))
print(test_data)

