import gspread
import time
import pprint

# <editor-fold desc="gs auth">
gs_name = 'scouting gamification'
path_to_gspread_credentials_json = '/Users/ysenkiv/Code/access files/personal/google sheets and drive for gspread/credentials.json'
path_to_gspread_authorized_user = '/Users/ysenkiv/Code/access files/personal/google sheets and drive for gspread/authorized_user.json'
google_client = gspread.oauth(credentials_filename=path_to_gspread_credentials_json, authorized_user_filename=path_to_gspread_authorized_user)
gs = google_client.open(gs_name)
score_log_sheet = gs.worksheet('score log')
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


def gather_sum_update_scores_from_main_sheet():
    scouts_mail_list = db_sheet.col_values(1)
    log_sheet_mails_list = score_log_sheet.col_values(2)

    for scout_mail in scouts_mail_list:
        if scout_mail in log_sheet_mails_list:
            scout_total_score = 0

            for row in range(2, len(log_sheet_mails_list) + 1):
                log_note = score_log_sheet.row_values(row)
                log_date = log_note[0]
                log_mail = log_note[1]
                log_activity = log_note[2]

                if log_mail not in scouts_mail_list:
                    continue
                else:
                    scout_total_score += activity_value(log_activity)
            row = scouts_mail_list.index(scout_mail) + 1
            col = get_col_num('scores', db_sheet)
            db_sheet.update_cell(row, col, scout_total_score)


def optimised_gather_sum_update_scores_from_main_sheet():
    lis = score_log_sheet.get_all_records()
    print(pprint.pformat(lis))


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
            nearest_free_row = len(score_log_sheet.col_values(1)) + 1
            last_future_row = nearest_free_row + len(log_notes_list)
            update_range = f'A{str(nearest_free_row)}:E{str(last_future_row)}'
            score_log_sheet.update(update_range, log_notes_list)
            gs.values_clear(f"{group_evaluation_sheet.title}!A2:J20")


# </editor-fold>
# migrate_scores_from_group_sheets_to_log_sheet()
optimised_gather_sum_update_scores_from_main_sheet()
# gather_sum_update_scores_from_main_sheet()








