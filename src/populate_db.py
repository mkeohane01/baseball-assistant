import sqlite3
import pandas as pd
from pybaseball import batting_stats, pitching_stats

def update_pitching_stats(year=2024):
    """
    Update the pitching stats database for the given year.
    """
    # Fetch pitching stats for the given year
    stats = pitching_stats(year, qual=20)
    # Select the relevant columns
    selected_columns = [
        'Name', 'Team', 'Age', 'W', 'L', 'WAR', 'ERA','G', 'GS', 'SV', 'IP', 
        'SO', 'BB', 'HR', 'WHIP', 'FIP', 'xFIP', 'K/9', 'BB/9', 'K%', 'BB%', 'BABIP', 'LOB%', 
        'Stuff+', 'Location+', 'Pitching+', 'xERA', 'HardHit%', 'CSW%'
    ]
    
    stats = stats[selected_columns]
    
    # Round all numerical columns to 2 decimal places
    for col in stats.columns:
        if stats[col].dtype in [float, int]:
            stats[col] = stats[col].round(2)
    # print(stats.head(2))
    print("\nPitcher db shape:")
    # print(stats.dtypes)
    print(stats.shape)
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('baseball_stats.db')
    cursor = conn.cursor()

    # Drop the existing table if it exists
    cursor.execute(f'DROP TABLE IF EXISTS PitchingStats{str(year)}')

    # Create a table for pitching stats if it doesn't exist
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS PitchingStats{str(year)} (
            ID INTEGER PRIMARY KEY,
            Name TEXT,
            Team TEXT,
            Age INTEGER,
            W INTEGER,
            L INTEGER,
            WAR REAL,
            ERA REAL,
            G INTEGER,
            GS INTEGER,
            SV INTEGER,
            IP REAL,
            SO INTEGER,
            BB INTEGER,
            HR INTEGER,
            WHIP REAL,
            FIP REAL,
            xFIP REAL,
            K9 REAL,
            BB9 REAL,
            KPercent REAL,
            BBPercent REAL,
            BABIP REAL,
            LOBPercent REAL,
            StuffPlus REAL,
            LocationPlus REAL,
            PitchingPlus REAL,
            xERA REAL,
            HardHitPercent REAL,
            CSWPercent REAL
        )
    ''')

    # Insert the stats into the database
    for _, row in stats.iterrows():
        cursor.execute(f'''
            INSERT OR REPLACE INTO PitchingStats{str(year)} (
                Name, Team, Age, W, L, WAR, ERA, G, GS, SV, IP, SO, BB, HR, WHIP, 
                FIP, xFIP, K9, BB9, KPercent, BBPercent, BABIP, LOBPercent, StuffPlus, LocationPlus, 
                PitchingPlus, xERA, HardHitPercent, CSWPercent
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['Name'], row['Team'], row['Age'], row['W'], row['L'], row['WAR'], 
            row['ERA'], row['G'], row['GS'], row['SV'], row['IP'], row['SO'], row['BB'], row['HR'], 
            row['WHIP'], row['FIP'], row['xFIP'], row['K/9'], row['BB/9'], row['K%'], row['BB%'], row['BABIP'], 
            row['LOB%'], row['Stuff+'], row['Location+'], row['Pitching+'], row['xERA'], row['HardHit%'], 
            row['CSW%']
        ))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()

def update_hitting_stats(year=2024):
    """
    Update the hitting stats database for the given year.
    """
    # Fetch hitting stats for the given year
    stats = batting_stats(year, qual=25)
    # Select the relevant columns
    selected_columns = [
        'Name', 'Team', 'Age', 'G', 'PA', 'AB', 'H', '1B', '2B', '3B', 'HR', 'R', 'RBI', 'BB', 
        'SO', 'HBP', 'SF', 'AVG', 'OBP', 'SLG', 'OPS', 'ISO', 'BABIP', 'wOBA', 'wRAA', 'wRC', 'wRC+', 
        'WAR', 'BsR', 'Spd', 'UBR', 'wSB', 'Off', 'Def', 'Pos', 'RAR', 'Barrel%', 'maxEV', 'HardHit%', 'CSW%', 
        'xBA', 'xSLG', 'xwOBA'
    ]
    stats = stats[selected_columns]

    # Round all numerical columns to 2 decimal places
    for col in stats.columns:
        if stats[col].dtype in [float, int]:
            stats[col] = stats[col].round(2)

    # print(stats.head(2))
    print("\nHitter db shape:")
    print(stats.shape)
    # Connect to SQLite database (or create it if it doesn't exist)
    conn = sqlite3.connect('baseball_stats.db')
    cursor = conn.cursor()

    # Drop the existing table if it exists
    cursor.execute(f'DROP TABLE IF EXISTS HittingStats{str(year)}')
    
    # Create a table for hitting stats if it doesn't exist
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS HittingStats{str(year)} (
            ID INTEGER PRIMARY KEY,
            Name TEXT,
            Team TEXT,
            Age INTEGER,
            G INTEGER,
            PA INTEGER,
            AB INTEGER,
            H INTEGER,
            Singles INTEGER,
            Doubles INTEGER,
            Triples INTEGER,
            HR INTEGER,
            R INTEGER,
            RBI INTEGER,
            BB INTEGER,
            SO INTEGER,
            HBP INTEGER,
            SF INTEGER,
            AVG REAL,
            OBP REAL,
            SLG REAL,
            OPS REAL,
            ISO REAL,
            BABIP REAL,
            wOBA REAL,
            wRAA REAL,
            wRC REAL,
            wRC_plus REAL,
            WAR REAL,
            BsR REAL,
            Spd REAL,
            UBR REAL,
            wSB REAL,
            Off REAL,
            Def REAL,
            Pos REAL,
            RAR REAL,
            Barrel_percent REAL,
            maxEV REAL,
            HardHit_percent REAL,
            CSW_percent REAL,
            xBA REAL,
            xSLG REAL,
            xwOBA REAL
        )
    ''')

    # Insert the stats into the database
    for _, row in stats.iterrows():
        cursor.execute(f'''
            INSERT OR REPLACE INTO HittingStats{str(year)} (
                Name, Team, Age, G, PA, AB, H, Singles, Doubles, Triples, HR, R, RBI, BB, 
                SO, HBP, SF, AVG, OBP, SLG, OPS, ISO, BABIP, wOBA, wRAA, wRC, wRC_plus, WAR, BsR, Spd, 
                UBR, wSB, Off, Def, Pos, RAR, Barrel_percent, maxEV, HardHit_percent, CSW_percent, xBA, xSLG, xwOBA
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            row['Name'], row['Team'], row['Age'], row['G'], row['PA'], row['AB'], row['H'], 
            row['1B'], row['2B'], row['3B'], row['HR'], row['R'], row['RBI'], row['BB'], row['SO'], 
            row['HBP'], row['SF'], row['AVG'], row['OBP'], row['SLG'], row['OPS'], row['ISO'], row['BABIP'], row['wOBA'], 
            row['wRAA'], row['wRC'], row['wRC+'], row['WAR'], row['BsR'], row['Spd'], row['UBR'], row['wSB'], row['Off'], 
            row['Def'], row['Pos'], row['RAR'], row['Barrel%'], row['maxEV'], row['HardHit%'], row['CSW%'], row['xBA'], 
            row['xSLG'], row['xwOBA']
        ))

    # Commit the transaction and close the connection
    conn.commit()
    conn.close()


if __name__ == '__main__':
    update_pitching_stats()
    update_hitting_stats()
    # Access the db with sqlite3 baseball_stats.db
    # Query for a player's stats: SELECT * FROM HittingStats2024 WHERE Name = 'CJ Abrams';
    conn = sqlite3.connect('baseball_stats.db')
    hitting_stats = pd.read_sql_query("SELECT * FROM HittingStats2024 WHERE Name = 'CJ Abrams'", conn)
    pitching_stats = pd.read_sql_query("SELECT * FROM PitchingStats2024 WHERE Name = 'DJ Herz'", conn)
    print(hitting_stats)
    print(pitching_stats)
