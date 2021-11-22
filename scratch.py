import gspread
"""score_sheet_list = score_sheet.get_all_values()
sum_email_col = sum_sheet.col_values(1)
print(score_sheet_list)


def activity_value(activity):
    if activity == 'гурткові сходини':
        value = 10
    if activity == 'курінні сходини':
        value = 15
    else:
        value = 5
    return value


for row in range(1, len(score_sheet_list)):
    print(score_sheet_list[row][0])
    print(score_sheet_list[row][1])
    if score_sheet_list[row][1] not in sum_email_col:
        print(score_sheet_list[row][1], 'not in sum sheet')
        sum_sheet.update(f'A{str(len(sum_email_col) + 1)}', score_sheet_list[row][1])
        sum_sheet.update(f'B{str(len(sum_email_col) + 1)}', activity_value(score_sheet_list[row][2]))
    else:
        print(score_sheet_list[row][1], 'in sum sheet')
    print(score_sheet_list[row][2])"""
"""import gspread

# <editor-fold desc="gs auth">
gs_name = 'пласт ігрифікація'
path_to_gspread_credentials_json = '/Users/ysenkiv/Code/access files/personal/google sheets and drive for gspread/credentials.json'
path_to_gspread_authorized_user = '/Users/ysenkiv/Code/access files/personal/google sheets and drive for gspread/authorized_user.json'
google_client = gspread.oauth(credentials_filename=path_to_gspread_credentials_json, authorized_user_filename=path_to_gspread_authorized_user)
gs = google_client.open(gs_name)
score_sheet = gs.worksheet('персональне')
sum_sheet = gs.worksheet('сума')
db_sheet = gs.worksheet('бд')
# </editor-fold>


def get_col_num(col_name_str, db_sheet_titles_list=db_sheet.row_values(1)):
    if col_name_str in db_sheet_titles_list:
        col_num = db_sheet_titles_list.index(col_name_str) + 1
    else:
        col_num = 'x'
    return col_num


print(get_col_num('пошта'))
print(get_col_num('курінь'))"""
"""list1 = list('QWERTYUI')
print(list1)
list1 = [element.lower() for element in list1]
print(list1)"""

gs_name = 'scouting gamification'
path_to_gspread_credentials_json = '/Users/ysenkiv/Code/access files/personal/google sheets and drive for gspread/credentials.json'
path_to_gspread_authorized_user = '/Users/ysenkiv/Code/access files/personal/google sheets and drive for gspread/authorized_user.json'
google_client = gspread.oauth(credentials_filename=path_to_gspread_credentials_json, authorized_user_filename=path_to_gspread_authorized_user)
gs = google_client.open(gs_name)
score_log_sheet = gs.worksheet('score log')
db_sheet = gs.worksheet('db')
test_sheet = gs.worksheet('test')

score_log_sheet.update(f'A1:D1', [['time_stamp', 'score', 'activity', 'who_evaluate']])
