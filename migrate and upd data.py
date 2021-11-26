import gspread
import time
import pprint

# <editor-fold desc="gs auth">
gs_name = 'scouting gamification'
path_to_gspread_credentials_json = '/Users/ysenkiv/Code/access files/personal/google sheets and drive for gspread/credentials.json'
path_to_gspread_authorized_user = '/Users/ysenkiv/Code/access files/personal/google sheets and drive for gspread/authorized_user.json'
google_client = gspread.oauth(credentials_filename=path_to_gspread_credentials_json, authorized_user_filename=path_to_gspread_authorized_user)
gs = google_client.open(gs_name)
log_sheet = gs.worksheet('score log')
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


def get_first_not_parsed_row():
    full_rows_num = len(log_sheet.col_values(get_col_num('parsed', log_sheet)))
    first_not_parsed_row = full_rows_num + 1
    return first_not_parsed_row


def migrate_additional_data_to_log_sheet():
    list_of_dics = db_sheet.get_all_records()
    start_row = get_first_not_parsed_row()
    range_to_update = f'F{str(start_row)}:O{str(len(log_sheet.col_values(2)))}'
    list_for_upd = []
    for mail in log_sheet.col_values(get_col_num('mail', log_sheet)):
        for dic in list_of_dics:
            if mail in dic.values():
                scout_list = [dic['first name'], dic['second name'], dic['sex'], dic['team'],
                              dic['troop'], dic['joined'], dic['born'], dic['age group'], dic['rank'], True]
                list_for_upd.append(scout_list)

    log_sheet.update(range_to_update, list_for_upd)


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


def migrate_scores_from_group_sheets_to_log_sheet():
    for group_evaluation_sheet in gs.worksheets():
        if group_evaluation_sheet.title.startswith('team'):
            lis = group_evaluation_sheet.get_all_records()
            log_notes_list = []
            for dic_row in lis:
                time_stamp = dic_row['Позначка часу']
                who_evaluate = dic_row['Електронна адреса']
                activity = dic_row['activity']
                for scout_key in dic_row:
                    if '.com' in scout_key:
                        scout = scout_key
                        scout_score = dic_row[scout_key]
                        log_row = [time_stamp, scout, scout_score, activity, who_evaluate]
                        log_notes_list.append(log_row)
                        print(log_row)
            # define range
            nearest_free_row = len(log_sheet.col_values(1)) + 1
            last_future_row = nearest_free_row + len(log_notes_list)
            update_range = f'A{str(nearest_free_row)}:E{str(last_future_row)}'
            log_sheet.update(update_range, log_notes_list)
            gs.values_clear(f"{group_evaluation_sheet.title}!A2:J20")


# </editor-fold>
migrate_additional_data_to_log_sheet()
# gather_sum_update_scores_from_main_sheet()
# migrate_scores_from_group_sheets_to_log_sheet()








