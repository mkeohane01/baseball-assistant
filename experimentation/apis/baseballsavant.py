from pybaseball import playerid_lookup, statcast_pitcher, statcast_batter

def get_player_id(lastname, firstname=None):
    player = playerid_lookup(lastname, first=firstname, fuzzy=True)
    return player.iloc[0]['key_mlbam']

def get_pitcher_stats(player_id, start_date='2024-06-01', end_date=None):
    return statcast_pitcher(start_date, end_date, player_id)

def get_batter_stats(player_id, start_date='2024-06-01', end_date=None):
    return statcast_batter(start_date, end_date, player_id)


if __name__ == '__main__':
    player = get_player_id('abrams', 'cj')
    print(player)
    stats = get_batter_stats(player, '2024-04-01', '2024-06-1')
    print(stats)