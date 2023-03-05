import ast
import code_diff as cd
import sys 

def probe_bugs(buggy, patched):
    bug_type_message = "Quantum error!"
    code_difference = cd.diff(buggy, patched)
    edit_script = code_difference.edit_script()
    # use a callback in bug_detectors/probe.py
    return bug_type_message

def process_files(): # You have to pass in the buggy fileaname directory first, followed by the patched one
    # Get the file names from command line arguments
    buggy = sys.argv[1]
    patched = sys.argv[2]

    # Read the files as strings
    with open(buggy, "r") as read_buggy:
        commented_buggy_src = read_buggy.read()

    with open(patched, "r") as read_patched:
        commented_patched_src = read_patched.read()
    
    return commented_buggy_src, commented_patched_src

def classify_bugs():
    buggy, patched = process_files()
    return probe_bugs(buggy, patched) # Mention line numbers, etc.?

if __name__ == "__main__":
    classify_bugs()
