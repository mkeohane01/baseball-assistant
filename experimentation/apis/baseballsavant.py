import pybaseball as pyb

pyb.cache.enable()

def get_player_id(lastname, firstname=None):
    player = pyb.playerid_lookup(lastname, first=firstname, fuzzy=True)
    return player.iloc[0]['key_mlbam']

def get_pitcher_statcast(player_id, start_date='2024-06-01', end_date=None):
    return pyb.statcast_pitcher(start_date, end_date, player_id)

def get_batter_statcast(player_id, start_date='2024-06-01', end_date=None):
    return pyb.statcast_batter(start_date, end_date, player_id)

def get_batting_stats(year):
    return pyb.batting_stats(year)

def get_top_prospects(team):
    return pyb.top_prospects(team)

def get_standings(year):
    return pyb.standings(year)

if __name__ == '__main__':
    player = get_player_id('abrams', 'cj')
    print(player)
    stats = get_batter_statcast(player, '2024-04-01')
    print(stats)
    batting_stats = get_batting_stats(2024)
    print(batting_stats.loc[batting_stats.Name == "CJ Abrams"])
    print(get_top_prospects("nationals"))
