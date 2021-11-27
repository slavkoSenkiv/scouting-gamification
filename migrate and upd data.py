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


# <editor-fold desc="functions">
def get_col_num(col_name_str, sheet):
    sheet_titles_list = sheet.row_values(1)
    sheet_lower_titles_list = [title.lower() for title in sheet_titles_list]

    if col_name_str in sheet_lower_titles_list:
        col_num = sheet_lower_titles_list.index(col_name_str)
    else:
        col_num = 'x'
    return col_num + 1


def activity_value(activity):
    if activity == 'гурткові сходини':
        value = 10
    elif activity == 'курінні сходини':
        value = 15
    else:
        value = 5
    return value


def define_score_origin(sheet_name):
    if sheet_name.startswith('team'):
        return 'team'


def optimised_migrate_scores_from_team_sheets_and_add_additional_data_from_db_sheet_to_log_sheet():
    for assessment_sheet in gs.worksheets():
        if assessment_sheet.title.startswith('team'):
            list_of_dicts_from_assessment_sheet = assessment_sheet.get_all_records()
            list_of_lists_for_log_sheet_upd = []
            for dict_row_from_assessment_sheet in list_of_dicts_from_assessment_sheet:
                for scout_mail in dict_row_from_assessment_sheet:
                    if '.com' in scout_mail:
                        # <editor-fold desc="getting dict_row_from_assessment_sheet time values">
                        time_string = dict_row_from_assessment_sheet['Позначка часу']
                        time_stamp = datetime.strptime(time_string, '%d.%m.%Y %H:%M:%S')
                        year = time_stamp.year - 2000
                        month = time_stamp.month
                        month_day = time_stamp.day
                        week_day = calendar.day_name[time_stamp.weekday()]
                        month_week = time_stamp.isocalendar()[1] - time_stamp.replace(day=1).isocalendar()[1] + 1
                        year_week = time_stamp.isocalendar().week
                        hour = time_stamp.hour
                        # </editor-fold>
                        score_origin = define_score_origin(assessment_sheet.title)
                        # print(year, month, month_day, week_day, month_week, year_week, hour, score_origin)
                        who_evaluate = dict_row_from_assessment_sheet['Електронна адреса']
                        activity = dict_row_from_assessment_sheet['activity']
                        scout_score = dict_row_from_assessment_sheet[scout_mail]
                        new_log_row_note = [time_string,
                                            scout_mail,
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
                        list_of_lists_for_log_sheet_upd.append(new_log_row_note)
                        # print(log_row)
            # ______
            list_of_dicts_from_db_sheet = db_sheet.get_all_records()
            first_not_parsed_row_num = len(log_sheet.col_values(get_col_num('parsed', log_sheet))) + 1
            range_to_update = f'N{str(first_not_parsed_row_num)}:W{str(len(log_sheet.col_values(2)))}'
            list_of_lists_for_log_sheet_upd = []
            for scout_mail in log_sheet.col_values(get_col_num('mail', log_sheet)):
                for dict_row in list_of_dicts_from_db_sheet:
                    if scout_mail in dict_row.values():
                        scout_list = [dict_row['first name'],
                                      dict_row['second name'],
                                      dict_row['sex'],
                                      dict_row['team'],
                                      dict_row['troop'],
                                      dict_row['joined'],
                                      dict_row['born'],
                                      dict_row['age group'],
                                      dict_row['rank'],
                                      True]  # parsed?
                        list_of_lists_for_log_sheet_upd.append(scout_list)

            log_sheet.update(range_to_update, list_of_lists_for_log_sheet_upd)
            first_empty_row_num = len(log_sheet.col_values(1)) + 1
            future_last_row_num = first_empty_row_num + len(list_of_lists_for_log_sheet_upd)
            update_range = f'A{str(first_empty_row_num)}:M{str(future_last_row_num)}'
            log_sheet.update(update_range, list_of_lists_for_log_sheet_upd)
            gs.values_clear(f"{assessment_sheet.title}!A2:J20")


def migrate_scores_from_group_sheets_to_log_sheet():
    for assessment_sheet in gs.worksheets():
        if assessment_sheet.title.startswith('team'):
            list_of_dicts_from_assessment_sheet = assessment_sheet.get_all_records()
            list_of_lists_for_log_sheet_upd = []
            for dict_row_from_assessment_sheet in list_of_dicts_from_assessment_sheet:
                for scout_mail in dict_row_from_assessment_sheet:
                    if '.com' in scout_mail:
                        # <editor-fold desc="getting dict_row_from_assessment_sheet time values">
                        time_string = dict_row_from_assessment_sheet['Позначка часу']
                        time_stamp = datetime.strptime(time_string, '%d.%m.%Y %H:%M:%S')
                        year = time_stamp.year - 2000
                        month = time_stamp.month
                        month_day = time_stamp.day
                        week_day = calendar.day_name[time_stamp.weekday()]
                        month_week = time_stamp.isocalendar()[1] - time_stamp.replace(day=1).isocalendar()[1] + 1
                        year_week = time_stamp.isocalendar().week
                        hour = time_stamp.hour
                        # </editor-fold>
                        score_origin = define_score_origin(assessment_sheet.title)
                        # print(year, month, month_day, week_day, month_week, year_week, hour, score_origin)
                        who_evaluate = dict_row_from_assessment_sheet['Електронна адреса']
                        activity = dict_row_from_assessment_sheet['activity']
                        scout_score = dict_row_from_assessment_sheet[scout_mail]
                        new_log_row_note = [time_string,
                                            scout_mail,
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
                        list_of_lists_for_log_sheet_upd.append(new_log_row_note)
                        # print(log_row)


def migrate_additional_data_to_log_sheet():
    list_of_dicts_from_db_sheet = db_sheet.get_all_records()
    first_not_parsed_row_num = len(log_sheet.col_values(get_col_num('parsed', log_sheet))) + 1
    range_to_update = f'N{str(first_not_parsed_row_num)}:W{str(len(log_sheet.col_values(2)))}'
    list_of_lists_for_log_sheet_upd = []
    for scout_mail in log_sheet.col_values(get_col_num('mail', log_sheet)):
        for dict_row in list_of_dicts_from_db_sheet:
            if scout_mail in dict_row.values():
                scout_list = [dict_row['first name'],
                              dict_row['second name'],
                              dict_row['sex'],
                              dict_row['team'],
                              dict_row['troop'],
                              dict_row['joined'],
                              dict_row['born'],
                              dict_row['age group'],
                              dict_row['rank'],
                              True]  # parsed?
                list_of_lists_for_log_sheet_upd.append(scout_list)

    log_sheet.update(range_to_update, list_of_lists_for_log_sheet_upd)


def gather_sum_update_scores_from_main_sheet():
    lis = log_sheet.get_all_records()
    log_summary = {}
    for log_row in lis:
        if log_row['scout'] not in log_summary.keys():
            if log_row['score'] == '':
                log_row['score'] = 0
            log_summary.setdefault(log_row['scout'], log_row['score'])
            continue  # in order to avoid next if for same scout

        if log_row['scout'] in log_summary.keys():
            if log_row['score'] == '':
                log_row['score'] = 0
            updated_score = log_summary[log_row['scout']] + log_row['score']
            log_summary[log_row['scout']] = updated_score

    scouts_list = db_sheet.col_values(1)
    for scout in log_summary:
        if scout in scouts_list:
            print(f'{scout} is in db')
            row = scouts_list.index(scout) + 1
            col = get_col_num('scores', db_sheet)
            score = log_summary[scout]
            db_sheet.update_cell(row, col, score)
        else:
            print(f'{scout} is not in db')
            row = len(db_sheet.col_values(1)) + 1
            score_col = get_col_num('scores', db_sheet)
            scout_col = get_col_num('mail', db_sheet)
            score = log_summary[scout]
            db_sheet.update_cell(row, score_col, score)
            db_sheet.update_cell(row, scout_col, scout)


# </editor-fold>
optimised_migrate_scores_from_team_sheets_and_add_additional_data_from_db_sheet_to_log_sheet()
# migrate_scores_from_group_sheets_to_log_sheet()
# migrate_additional_data_to_log_sheet()
# gather_sum_update_scores_from_main_sheet()








