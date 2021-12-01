situations = {'one_player': {'p1': 1},
              'all_players_have_different_places': {'p1': 1,
                                                    'p2': 2,
                                                    'p3': 3,
                                                    'p4': 4,
                                                    'p5': 5,
                                                    'p6': 6,
                                                    'p7': 7,
                                                    'p8': 8,
                                                    'p9': 9,
                                                    'p10': 10},
              'some_players_have_similar_places': {'p1': 1,
                                         'p2': 2,
                                         'p3': 2,
                                         'p4': 3,
                                         'p5': 3,
                                         'p6': 4,
                                         'p7': 4,
                                         'p8': 4,
                                         'p9': 4,
                                         'p10': 4}}


def get_coefficient(player_name, player_place, places):
    coefficient = 150 - ((player_place - 1) * 150 / places)
    print(f'{player_name} with {player_place} place has {coefficient} coef')


def get_places_num(dict):
    lis = []
    for k, v in dict.items():
        if v not in lis:
            lis.append(v)
    return len(lis)


for situation_name, players_and_places in situations.items():
    print(situation_name)
    for player_name, player_place in players_and_places.items():
        get_coefficient(player_name, player_place, get_places_num(players_and_places))
    print()
