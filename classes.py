import gspread


# <editor-fold desc="gs auth">
gs_name = 'scouting gamification'
path_to_gspread_credentials_json = '/Users/ysenkiv/Code/access files/personal/google sheets and drive for gspread/credentials.json'
path_to_gspread_authorized_user = '/Users/ysenkiv/Code/access files/personal/google sheets and drive for gspread/authorized_user.json'
google_client = gspread.oauth(credentials_filename=path_to_gspread_credentials_json, authorized_user_filename=path_to_gspread_authorized_user)
gs = google_client.open(gs_name)
score_log_sheet = gs.worksheet('score log')
db_sheet = gs.worksheet('db')
# </editor-fold>

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