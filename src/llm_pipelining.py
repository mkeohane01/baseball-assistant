import pybaseball as pyb
import difflib
import json
from src.utils import query_llm_llamafile, get_batting_stats, get_pitching_stats

    
def extract_player_llm(user_input):
    # Extract player name from this user question
    sys_prompt = '''
    Your sole purpose is to extract a list of player names from the user input.
    The input will be some sort of question or statement that contains one or more player names.
    You should extract all of the player names from the input and return them as a list.
    DO NOT RETURM ANYHING ELSE EXCEPT THE PLAYER NAME LIST!!!

    Examples:
    Input: "How well are CJ Abrams and DJ Herz doing this season?"
    Ouput: ["CJ Abrams", "DJ Herz"]

    Input: "Should I trade Pual Goldschmidt for Jake Irvin?"
    Output: ["Paul Goldschmidt", "Jake Irvin"]

    Input: "What is Luis Garcia's batting average?"
    Output: ["Luis Garcia"]
    '''
    response = query_llm_llamafile(user_input, sys_prompt)
    return response


def get_player_stats(players: list):
    """
    Get all of the stats for a list of MLB players, searching both hitting and pitching stats.
    Args:
        players - list of player full names
    Returns:
        A dictionary where keys are player names and values are dictionaries containing their stats
    """
    player_stats_dict = {}

    for player in players:
        hit_status, hit_stats = get_batting_stats(player)
        pitch_status, pitch_stats = get_pitching_stats(player)
        
        if hit_status == 200:
            player_stats_dict[player] = {
                "Type": "Hitter",
                "Stats": hit_stats
            }
        elif pitch_status == 200:
            player_stats_dict[player] = {
                "Type": "Pitcher",
                "Stats": pitch_stats
            }
        elif hit_status == 405:
            player_stats_dict[player] = {
                "Type": "Unknown",
                "Message": hit_stats  # The 405 message from hitting stats
            }
        elif pitch_status == 405:
            player_stats_dict[player] = {
                "Type": "Unknown",
                "Message": pitch_stats  # The 405 message from pitching stats
            }
        elif hit_status == 404 and pitch_status == 404:
            player_stats_dict[player] = {
                "Type": "Unknown",
                "Message": "Unable to find player."
            }

    return player_stats_dict

def answer_baseball_question(user_question):
    """
    Given a user question, return the answer using the LLM model after 
    extracting the players and retrieveing their respective stats.

    Args:
        user_question - string of the user's question
    Returns:
        string of the model's response
    """
    extracted_players = extract_player_llm(user_question)
    parsed_players = json.loads(extracted_players)
    print(f"Extracted players: {parsed_players}")
    player_stats = get_player_stats(parsed_players)
    print(f"Player stats: {player_stats}")
    return player_stats

if __name__ == '__main__':
    players = ["CJ Abrms", "DJ Herz", "Jake Irvin"]
    player_stats = get_player_stats(players)
    print(player_stats)