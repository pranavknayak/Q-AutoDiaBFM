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
    codeSample = (buggy, codeDifference.edit_script(), patched)
    status, bugTypeMessage = prober.assessBugClass(bugDataRootDirectoryName, codeSample,
                                                  threadingStyle.nil.value)
    if status == False: # Or that there is a bug category which we are unable to identify (captured by msg below already)
        bugTypeMessage = "No quantum error detected!"
    return bugTypeMessage

def processFiles(buggy = None, patched = None, commandLine = True): # The buggy filename directory first, followed by the patched one.
    # Get the file names from command line arguments.
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
