from openai import OpenAI
import sqlite3
import difflib

DATABASE = 'baseball_stats.db'

def query_llm_llamafile(user_prompt, system_prompt):
    """
    Query the llamafile model with a user prompt and system prompt'
    Args:
        user_prompt - string of user input
        system_prompt - string of system input
    Returns:
        response - string of response from the llamafile model
    """
    client = OpenAI(
        base_url= "http://127.0.0.1:8080/v1", # "http://<Your api-server IP>:port"
        api_key = "sk-no-key-required"
    )
    completion = client.chat.completions.create(
        model="LLaMA_CPP",
        max_tokens = 150,
        temperature = 0,
        messages=[
            {"role": "system", "content": 
             system_prompt
             },
            {"role": "user", "content": f"<human_start>{user_prompt}<human_end>"}
        ]
    )
    return completion.choices[0].message.content.split('<|')[0]


def get_batting_stats(player: str):
    """
    Get all of the hitting statistics for a specified MLB player from the HittingStats2024 table.
    Args:
        player - string of player full name
    Returns:
        if player exists:
            (status_code, batting_stats) - 200 and a list of stats for the specified player
        else:
            (status_code, error_message) - 404 and a string error message suggesting similar player names
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = "SELECT * FROM HittingStats2024 WHERE Name = ?"
    cursor.execute(query, (player,))
    player_stats = cursor.fetchall()

    if player_stats:
        conn.close()
        return 200, player_stats
    else:
        cursor.execute("SELECT Name FROM HittingStats2024")
        all_names = [row[0] for row in cursor.fetchall()]
        similar_names = difflib.get_close_matches(player, all_names)
        conn.close()
        if similar_names:
            return 405, f"Unable to find player. Did you mean: {', '.join(similar_names)}?"
        else:
            return 404, "Unable to find player."

def get_pitching_stats(player: str):
    """
    Get all of the pitching statistics for a specified MLB player from the PitchingStats2024 table.
    Args:
        player - string of player full name
    Returns:
        if player exists:
            (status_code, pitching_stats) - 200 and a list of stats for the specified player
        else:
            (status_code, error_message) - 404 and a string error message suggesting similar player names
    """
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    query = "SELECT * FROM PitchingStats2024 WHERE Name = ?"
    cursor.execute(query, (player,))
    player_stats = cursor.fetchall()

    if player_stats:
        conn.close()
        return 200, player_stats
    else:
        cursor.execute("SELECT Name FROM PitchingStats2024")
        all_names = [row[0] for row in cursor.fetchall()]
        similar_names = difflib.get_close_matches(player, all_names)
        conn.close()
        if similar_names:
            return 405, f"Unable to find player. Did you mean: {', '.join(similar_names)}?"
        else:
            return 404, "Unable to find player."


if __name__ == '__main__':
    print(get_batting_stats("CJ Abras"))
    print(get_pitching_stats("Jake Irvin"))