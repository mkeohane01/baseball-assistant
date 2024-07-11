import pybaseball as pyb
import difflib
from openai import OpenAI


def get_batting_stats(player: str = None, year: int = 2024):
    """
    Get all of the hitting statistics for a specified MLB player
    Args:
        player - string of player full name
        year - year to get stats for, default is 2024 the current year
    Returns:
        if player exists:
            batting_stats - a list of stats for the specified player
        else:
            string error message suggesting similar player names
    """
    all_batting_stats = pyb.batting_stats(year)
    if player:
        if player in all_batting_stats['Name'].values:
            return all_batting_stats.loc[all_batting_stats.Name == player]
        else:
            # Find and suggest similar names
            similar_names = difflib.get_close_matches(player, all_batting_stats['Name'].values)
            if similar_names:
                return f"Unable to find player. Did you mean: {', '.join(similar_names)}?"
            else:
                return "Unable to find player."
    else:
        return all_batting_stats

def get_pitching_stats(player: str = None, year: int = 2024):
    """
    Get all of the pitching statistics for a specified MLB player
    Args:
        player - string of player full name
        year - year to get stats for, default is 2024 the current year
    Returns:
        if player exists:
            pitching_stats - a list of stats for the specified player
        else:
            string error message suggesting similar player names
    """
    all_pitching_stats = pyb.pitching_stats(year)
    if player:
        if player in all_pitching_stats['Name'].values:
            return all_pitching_stats.loc[all_pitching_stats.Name == player]
        else:
            # Find and suggest similar names
            similar_names = difflib.get_close_matches(player, all_pitching_stats['Name'].values)
            if similar_names:
                return f"Unable to find player. Did you mean: {', '.join(similar_names)}?"
            else:
                return "Unable to find player."
    else:
        return all_pitching_stats
    
#!/usr/bin/env python3
def query_llm_functions(prompt):
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
             """
             You are Baseball Helper 5000, an AI assistant. 
             Your top priority is determining which helpful baseball stats function to call based on the user input.
             Based on the user input, determine the player they are asking about as well as whether they are a batter or a pitcher.
             If you cannot determine this, ask a clarifying question, otherwise call the corresponding function.
             NO EXPLANATIONS!
             If multiple calls are needed, call all of the corresponding functions.    
             Function:
                def get_batting_stats(player: str = None, year: int = 2024):
                    ""
                    Get all of the hitting statistics for a specified MLB player
                    Args:
                        player - string of player full name
                        year - year to get stats for, default is 2024 the current year
                    Returns:
                        if player exists:
                            batting_stats - a list of stats for the specified player
                        else:
                            string error message suggesting similar player names
                    ""
            Function:
                def get_pitching_stats(player: str = None, year: int = 2024):
                    ""
                    Get all of the pitching statistics for a specified MLB player
                    Args:
                        player - string of player full name
                        year - year to get stats for, default is 2024 the current year
                    Returns:
                        if player exists:
                            pitching_stats - a list of stats for the specified player
                        else:
                            string error message suggesting similar player names
                    ""
            JUST GIVE POPULATED CALL FUNCTION, NO THOUGHT OR EXPLANATION!
            """
             },
            {"role": "user", "content": f"{prompt}<human_end>"}
        ]
    )
    return completion.choices[0].message

if __name__ == '__main__':
    print(get_batting_stats("CJ Abras"))
    print(get_pitching_stats("Jake Irvin"))
    response = query_llm_functions("How is CJ Abrams, hitter, and Jake Irvin, pitcher, performing this year?")
    print(response)