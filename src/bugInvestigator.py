""" This code imports essential modules like ast, code_diff, importlib, os, sys, and Enum, and defines threadingStyle enum.
It then defines findProbeFile and probeBugs functions to output a bugTypeMessage based on buggy and patched code samples and
uses processFiles and probeBugs functions to classify the bugs in the given code samples.
"""

import importlib
import os
import sys
from enum import Enum

""" Setting the root of the bugDetector tree."""
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
        # print(errorMessage)
        pass
    finally:
        return


def probeBugs(buggy, patched):
    findProbeFile()
    """ Setting the pointer to the root of the bugDetector tree."""
    prober = importlib.import_module(
        bugDataRootDirectoryName + "." + bugPruningFileName, bugPruningFilePath
    )
    """ Ideally passes the triplet (buggy, patched, f(buggy, patched)) down the tree. However, f = phi currently."""
    codeSample = (buggy, patched)
    """ Assesses the bug-fix class to which the bug fix pattern belongs to."""
    status, bugTypeMessage = prober.assessBugClass(
        bugDataRootDirectoryName, codeSample, threadingStyle.nil.value
    )
    """ Either there is no bug or there is a bug-fix pattern that evades detection from the currently
        implemented classifiers.
    """
    if status == False:
        bugTypeMessage['default'] = ["No quantum error detected!"]
    return bugTypeMessage


def processFiles(buggy=None, patched=None, commandLine=True):
    """Get the file names from command line arguments. Parses the code snippets as strings."""
    commentedBuggySrc = ""
    commentedPatchedSrc = ""
    if commandLine == True:
        buggy = sys.argv[1]
        patched = sys.argv[2]

        with open(buggy, "r") as readBuggy:
            commentedBuggySrc = readBuggy.read()

        with open(patched, "r") as readPatched:
            commentedPatchedSrc = readPatched.read()
    else:
        commentedBuggySrc = str(buggy)
        commentedPatchedSrc = str(patched)

    return commentedBuggySrc, commentedPatchedSrc


def classifyBugs(buggy=None, patched=None, commandLine=True):
    buggy, patched = processFiles(buggy, patched, commandLine)
    return probeBugs(buggy, patched)
