import ast
import code_diff
import importlib
import os
import sys
from enum import Enum

bugDataRootDirectoryName = "bugDetectors"
bugDataRootDirectoryPath = "../Q-AutoDiaBFM/src/bugDetectors"
bugPruningFileName = "probe"
bugPruningFilePath = bugDataRootDirectoryPath + "/" + bugPruningFileName + ".py"

class threadingStyle(Enum):
    nil = 0
    full = 1
    random = 2

def findProbeFile():
    try:
        assert os.path.exists(bugPruningFilePath), "No 'probe.py' file detected."
    except AssertionError as errorMessage:
        print(errorMessage)
    finally:
        return # do we return anything here?

def probeBugs(buggy, patched):
    codeDifference = code_diff.difference(buggy, patched, lang='python')
    findProbeFile()
    prober = importlib.import_module(bugDataRootDirectoryName + "." + bugPruningFileName,
                                      bugPruningFilePath)
    status, bugTypeMessage = prober.assessBugType(bugDataRootDirectoryName, codeDifference.edit_script(),
                                                  threadingStyle.nil.value)
    if status == False:
        bugTypeMessage = "No quantum error detected!"
    return bugTypeMessage

def processFiles(buggy = None, patched = None, commandLine = True): # You have to pass in the buggy fileaname directory first, followed by the patched one
    # Get the file names from command line arguments
    commentedBuggySrc = ""
    commentedPatchedSrc = ""
    if commandLine == True:
        buggy = sys.argv[1]
        patched = sys.argv[2]

        # Read the files as strings
        with open(buggy, "r") as readBuggy:
            commentedBuggySrc = readBuggy.read()

        with open(patched, "r") as readPatched:
            commentedPatchedSrc = readPatched.read()
    else:
        commentedBuggySrc = str(buggy)
        commentedPatchedSrc = str(patched)
    
    return commentedBuggySrc, commentedPatchedSrc

def classifyBugs(buggy = None, patched = None, commandLine = True):
    buggy, patched = processFiles(buggy, patched, commandLine)
    return probeBugs(buggy, patched) # Mention line numbers, etc.?
