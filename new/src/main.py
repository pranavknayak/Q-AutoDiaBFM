import os
import traceback
from BugInvestigator import BugInvestigator
from CodeProcessor import CodeProcessor

if __name__ == "__main__":
    # Initialize BugInvestigator
    bug_investigator = BugInvestigator("BugDetectors/config.json")
    bug_investigator.build_class_hierarchy()

    # Initialize the bug vector
    bug_vector = [0, 0, 0, 0, 0, 0, 0]

    # Path to the directory containing test folders
    testcases_dir = "../tests"

    # Iterate through test folders
    for folder_name in os.listdir(testcases_dir):
        folder_path = os.path.join(testcases_dir, folder_name)
        if os.path.isdir(folder_path) and folder_name.startswith("test_"):
            # Extract test number
            test_number = folder_name.split("_")[1]

            # Define buggy and fixed file paths
            buggy_file = os.path.join(folder_path, f"{test_number}_buggy.py")
            fixed_file = os.path.join(folder_path, f"{test_number}_fixed.py")

            # Check if both files exist
            if os.path.isfile(buggy_file) and os.path.isfile(fixed_file):
                try:
                    # Read buggy and fixed code
                    buggy_code = open(buggy_file, "r").read()
                    fixed_code = open(fixed_file, "r").read()

                    # Process the code
                    test = CodeProcessor(buggy_code, fixed_code)

                    # Detect patterns
                    bugErrorMessage = bug_investigator.detect_pattern(test)
                    print(f"Results for {folder_name}: {bugErrorMessage}")

                    # Update bug vector
                    if bugErrorMessage['Unitary'] != 'None':
                        if "Incorrect usage of built-in gate(s) and Incorrect usage of opaque gate(s)." in bugErrorMessage['Unitary']:
                            bug_vector[4] += 1
                            bug_vector[5] += 1
                        elif "Incorrect usage of built-in gate(s)." in bugErrorMessage['Unitary']:
                            bug_vector[4] += 1
                        elif "Incorrect usage of opaque gate(s)." in bugErrorMessage['Unitary']:
                            bug_vector[5] += 1

                        if "Unclosed Hadamard gate detected." in bugErrorMessage['IncorrectHadamard']:
                            bug_vector[6] += 1

                    if bugErrorMessage['Measurement'] != 'None':
                        if "Measurement(s) performed incorrectly and Excessive measurements performed." in bugErrorMessage['IncorrectMeasurement']:
                            bug_vector[2] += 1
                            bug_vector[3] += 1
                        elif "Measurement(s) performed incorrectly." in bugErrorMessage['IncorrectMeasurement']:
                            bug_vector[2] += 1
                        elif "Excessive measurements performed." in bugErrorMessage['IncorrectMeasurement']:
                            bug_vector[3] += 1

                    if bugErrorMessage['Initialization'] != 'None':
                        if "Incorrect initialization(s) attempted." in bugErrorMessage['IncorrectInit']:
                            bug_vector[0] += 1
                        if "Unequal bits vs. qubits during QuantumCircuit initialization(s)." in bugErrorMessage['IncorrectInit']:
                            bug_vector[1] += 1

                except BaseException as e:
                    print(f"ERROR AT {folder_name}")
                    print(traceback.format_exc())

    print("Final Bug Vector:", bug_vector)