import os
from xtractor.core import grail_extractor
import json

"""
This module is dedicated to test our protocol output using gpt
"""


def run_test():
    test_folder_path = 'case'
    for folder_name in os.listdir(test_folder_path):
        folder_path = os.path.join(test_folder_path, folder_name)
        if os.path.isdir(folder_path):
            # For each problem file
            for file_name in os.listdir(folder_path):
                if file_name.endswith('.txt'):
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'r') as file:
                        text = file.read()

                    # Extract relevant data from the text
                    result = grail_extractor(text)

                    # Save text output in file
                    result_file_path = os.path.join(folder_path, 'result.json')
                    with open(result_file_path, 'w') as result_file:
                        json.dump(result, result_file)


def run_specific_test(folder: str):
    folder_path = os.path.join('case', folder)
    if os.path.isdir(folder_path):
            # For each problem file
            for file_name in os.listdir(folder_path):
                if file_name.endswith('problem.txt'):
                    file_path = os.path.join(folder_path, file_name)
                    with open(file_path, 'r') as file:
                        text = file.read()

                    # Extract relevant data from the text
                    result = grail_extractor(text)

                    print("TEST: SEE OUTPUT IN RESULT.TXT FILE")

                    # Save text output in file
                    result_file_path = os.path.join(folder_path, 'result.json')
                    with open(result_file_path, 'w') as result_file:
                        json.dump(result, result_file)


if __name__ == '__main__':
    """
    Run all test case in test/case folder
    """
    # run_test()

    """
    Function description: This function is used to run a specific test. To use this function, pass the name 
        of the test folder as an argument. The corresponding test folder should be placed in the 'test/case' 
        directory. The test folder should contain two files: 'problem.txt' which contains the problem descr-
        iption in any language, and 'result.json' which is an empty file.

    Function input(s): test_folder_name (string): The name of the test folder to be run.
    
    Function output(s): Json. The function runs the specified test and return a json strong stored into 
        result.json.
    """
    run_specific_test('case_02_tennis')
