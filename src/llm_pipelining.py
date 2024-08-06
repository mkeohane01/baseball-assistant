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
    return json.loads(response)


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

def generate_response_using_data(user_question, player_stats_dict):
    """
    Generate an answer to the user's question based on a dictionary of player stats.

    Args:
        user_input (str): The original user question.
        player_stats_dict (dict): A dictionary where keys are player names and values are dictionaries 
                                  containing 'Type' and 'Stats' for each player.

    Returns:
        str: The generated answer based on the player's stats.
    """
    # Format the player stats dictionary into a string for the LLM prompt
    formatted_stats = ""
    for player, details in player_stats_dict.items():
        player_type = details["Type"]
        if player_type == "Unknown":
            error = details["Message"]
            formatted_stats += f"{player} : {error}\n"
        else:
            stats = details["Stats"]
            stats_str = ", ".join(f"{key}: {value}" for key, value in stats.items())
            formatted_stats += f"{player} ({player_type}): {stats_str}\n"

    sys_prompt = f'''
    Your task is to provide an answer to the following baseball related question based on the given player stats.
    Please use your prior knowlege of baseball to analyze these stats and make an educated response.
    Use the player names and their stats from the dictionary to generate a relevant answer.
    Here is the dictionary of player stats:
    
    {formatted_stats}
    
    Generate a clear and concise answer to the question using the provided stats. 
    Ensure the answer is specific to the question and uses the useful parts of the data effectively.
    '''
    
    response = query_llm_llamafile(user_question, sys_prompt)
    return response




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
    print(f"Extracted players: {extracted_players}")
    player_stats = get_player_stats(extracted_players)
    print(f"Player stats: {player_stats}")
    response = generate_response_using_data(user_question, player_stats)
    return response

if __name__ == '__main__':
    players = ["CJ Abrms", "DJ Herz", "Jake Irvin"]
    player_stats = get_player_stats(players)
    print(player_stats)