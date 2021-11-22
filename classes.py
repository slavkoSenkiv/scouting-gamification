import gspread
import time

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


def get_scout_attribute(scout_value_title, scout_row_values_list):
    try:
        mail = scout_row_values_list[get_col_num(scout_value_title, db_sheet)]
    except IndexError:
        mail = None
    except TypeError:
        print('!!! possibly some attributes names are written incorrectly in the code')
    return mail


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


def migrate_scores_from_group_sheets_to_log_sheet():
    scouts_mail_list = db_sheet.col_values(1)
    for group_evaluation_sheet in gs.worksheets():
        if group_evaluation_sheet.title.startswith('team'):
            activity_col_num = get_col_num('activity', group_evaluation_sheet)
            scouts_list = group_evaluation_sheet.row_values(1)[2:-1]
            for row in range(2, len(group_evaluation_sheet.col_values(1))):
                print(f'row in group_evaluation_sheet is {row}')
                for scout in scouts_list:
                    if scout[2:-1] not in scouts_mail_list:
                        print(f'{scout[2:-1]} not in db')
                    else:
                        print('scout', scout)

                        scout_col_num = get_col_num(scout, group_evaluation_sheet)
                        print('scout_col_num', scout_col_num)

                        # row then col
                        time_stamp = group_evaluation_sheet.cell(2, 1).value
                        print('time_stamp', time_stamp)

                        who_evaluate = group_evaluation_sheet.cell(2, 2).value
                        print('who_evaluate', who_evaluate)

                        score = group_evaluation_sheet.cell(2, scout_col_num).value
                        print('score', score)

                        activity = group_evaluation_sheet.cell(2, activity_col_num).value
                        print('activity', activity)

                        next_free_row = len(score_log_sheet.col_values(1)) + 1
                        print('next_free_row', next_free_row)

                        score_log_sheet.update(f'A{str(next_free_row)}:E{str(next_free_row)}', [[time_stamp, scout[2:-1], score, activity, who_evaluate]])
                group_evaluation_sheet.delete_rows(2, 2)
                print()

# </editor-fold>
# gather_sum_update_scores_from_main_sheet()
migrate_scores_from_group_sheets_to_log_sheet()


class Scout:
    def __init__(self, scout_row):
        # <editor-fold desc="rename">
        scout_row_values_list = db_sheet.row_values(scout_row)

        mail = get_scout_attribute('mail', scout_row_values_list)
        first_name = get_scout_attribute('first name', scout_row_values_list)
        second_name = get_scout_attribute('second name', scout_row_values_list)
        team = get_scout_attribute('team', scout_row_values_list)
        troop = get_scout_attribute('troop', scout_row_values_list)
        joined = get_scout_attribute('joined', scout_row_values_list)
        rank = get_scout_attribute('rank', scout_row_values_list)
        scores = get_scout_attribute('scores', scout_row_values_list)

        # </editor-fold>
        self.mail = mail
        self.first_name = first_name
        self.second_name = second_name
        self.team = team
        self.troop = troop
        self.joined = joined
        self.rank = rank
        self.scores = scores





