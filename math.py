def get_places_num(dic):
    lis = []
    for k, v in dic.items():
        if v not in lis:
            lis.append(v)
    return len(lis)


def get_coefficient(name, place, places):
    if place >= 1:
        coefficient = round(100 - ((place - 1) * 100 / places))
    if place < 1:
        coefficient = round(100 * place)
    print(f'{name} with {place} place has {coefficient} coef')


def iterate(dic):
    for name, place in dic.items():
        get_coefficient(name, place, get_places_num(dic))
        print('places', get_places_num(dic))
    print()


situations = {'one player done 100%':
                  {'p1': 1},

              'one player done 60%':
                  {'p1': 0.6},

              'one player done 0%':
                  {'p1': 0},

              'one player done -50%':
                  {'p1': -0.5},

              'one player done -100%':
                  {'p1': -1},

              'all players have different places':
                  {'p1': 1,
                   'p2': 2,
                   'p3': 3,
                   'p4': 4,
                   'p5': 5},

              'some players have similar places':
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
