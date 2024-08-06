import sys
import os
# Add the root directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import time
from src.llm_pipelining import extract_player_llm, answer_baseball_question

def test_extract_player_names(test_set):
    """
    Testing the extract_player_llm function with a set of test cases.
    """
    total_tests = len(test_set)
    passed_tests = 0
    total_time = 0
    print("-----Testing Player Name Extraction-----")
    print(f"Running {total_tests} tests...")
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


def test_pipeline_and_export(test_set, output_file="test_results.json"):
    """
    Test the whole LLM pipeline
    Export the results to a JSON file
    """
    total_time = 0
    results = []

    print("-----Testing LLM Pipeline-----")
    print(f"Running {len(test_set)} tests...")
    for test_case in test_set:
        question = test_case["input"]
        
        start_time = time.time()
        response = answer_baseball_question(question)
        end_time = time.time()
        
        elapsed_time = end_time - start_time
        total_time += elapsed_time
        
        results.append({"input": question, "output": response, "time": elapsed_time})
        print(f"input: {question}, output: {response}, time {elapsed_time}")

    average_time = total_time / len(test_set)

    with open(output_file, "w") as file:
        json.dump(results, file, indent=4)

    print(f"Results exported to {output_file}")
    print(f"Average Time per Question: {average_time} seconds")

if __name__ == "__main__":

    # Load the test set
    with open("tests/extraction_test_set.json", "r") as file:
        test_set = json.load(file)

    test_extract_player_names(test_set)
    test_pipeline_and_export(test_set, "tests/pipeline_results.json")