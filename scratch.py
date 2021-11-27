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
# </editor-fold>


def week_number_of_month(date_value):
    return (date_value.isocalendar()[1] - date_value.replace(day=1).isocalendar()[1] + 1)


def define_score_origin(sheet_name):
    if sheet_name.startswith('team'):
        return 'team'


def migrate_scores_from_group_sheets_to_log_sheet():
    for group_evaluation_sheet in gs.worksheets():
        if group_evaluation_sheet.title.startswith('team'):
            list_of_dicts = group_evaluation_sheet.get_all_records()
            log_sheet_list_of_lists_update = []
            for dict_row in list_of_dicts:
                for scout_key in dict_row:
                    if '.com' in scout_key:
                        # <editor-fold desc="get time values">
                        time_string = dict_row['Позначка часу']
                        time_stamp = datetime.strptime(time_string, '%d.%m.%Y %H:%M:%S')
                        year = time_stamp.year
                        month = time_stamp.month
                        month_day = time_stamp.day
                        week_day = calendar.day_name[time_stamp.weekday()]
                        month_week = week_number_of_month(time_stamp)
                        year_week = time_stamp.isocalendar().week
                        hour = time_stamp.hour
                        # </editor-fold>
                        score_origin = define_score_origin(group_evaluation_sheet.title)
                        print(year, month, month_day, week_day, month_week, year_week, hour, score_origin)

                        who_evaluate = dict_row['Електронна адреса']
                        activity = dict_row['activity']
                        scout = scout_key
                        scout_score = dict_row[scout_key]
                        log_row = [time_stamp,
                                   scout,
                                   scout_score,
                                   activity,
                                   who_evaluate,
                                   year,
                                   month,
                                   month_day,
                                   week_day,
                                   month_week,
                                   year_week,
                                   hour,
                                   score_origin]
                        log_sheet_list_of_lists_update.append(log_row)
                        # print(log_row)


migrate_scores_from_group_sheets_to_log_sheet()