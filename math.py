def get_places_num(dic):
    lis = []
    for k, v in dic.items():
        if v not in lis:
            lis.append(v)
    return len(lis)


def get_coefficient(name, place, places):
    if place >= 1:
        coefficient = round(100 - ((place - 1) * 100 / places), 2)
    if 1 > place >= 0:
        coefficient = round(100 * place, 2)
    if place < 0:
        coefficient = round(100 * place, 2)
    print(f'{name} with {place} place has {coefficient} coef')


def iterate(dic):
    for name, place in dic.items():
        get_coefficient(name, place, get_places_num(dic))
        print('places', get_places_num(dic))
    print()


situations = {'one_player_done_well':
                  {'p1': 1},

              'one_player_done_0.6':
                  {'p1': 0.6},

              'one_player_done_0':
                  {'p1': 0},

              'one_player_done -0.5':
                  {'p1': -0.5},

              'one_player_done_negative_1':
                  {'p1': -1},

              'all_players_have_different_places':
                  {'p1': 1,
                   'p2': 2,
                   'p3': 3,
                   'p4': 4,
                   'p5': 5},

              'some_players_have_similar_places':
                  {'p1': 1,
                   'p2': 2,
                   'p3': 2,
                   'p4': 3,
                   'p5': 4}}


for situation_name, players_and_places in situations.items():
    print(situation_name)
    for player_name, player_place in players_and_places.items():
        get_coefficient(player_name, player_place, get_places_num(players_and_places))
    print()
