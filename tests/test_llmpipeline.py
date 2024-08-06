import sys
import os
# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import time
from src.llm_pipelining import extract_player_llm

def test_extract_player_names(test_set):
    """
    Testing the extract_player_llm function with a set of test cases.
    """
    total_tests = len(test_set)
    passed_tests = 0
    total_time = 0

    for test in test_set:
        input_question = test["input"]
        expected_output = test["output"]
        
        start_time = time.time()
        actual_output = extract_player_llm(input_question)
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        total_time += elapsed_time

        if actual_output == expected_output:
            passed_tests += 1
        else:
            print(f"Test failed for input: {input_question}")
            print(f"Expected output: {expected_output}")
            print(f"Actual output: {actual_output}")
            print()

    average_time = total_time / total_tests
    print(f"Passed {passed_tests} out of {total_tests} tests.")
    print(f"Average time per test: {average_time:.6f} seconds")
    return passed_tests, total_tests, average_time

if __name__ == "__main__":

    # Load the test set
    with open("tests/extraction_test_set.json", "r") as file:
        test_set = json.load(file)

    test_extract_player_names(test_set)
