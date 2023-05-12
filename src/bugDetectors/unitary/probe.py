""" The code imports some modules such as threading, os, importlib, and Path. 
It defines two functions, "assessBugClass" and "assessBugType", 
which are used to assess bug classes and bug types, respectively.
"""

from bugInvestigator import threadingStyle
import importlib
import os
from pathlib import Path

""" In the "assessBugClass" function, there is a boolean variable "prune" initialized to False. 
The function takes a code sample as input and returns the "prune" variable. 
It does not appear to modify the input code sample. 
It is not clear what this function is used for as it does not perform any operation on the input.
"""


def assessBugClass(codeSample):
    prune = True
    """ Add in the short signature code here."""
    return prune


""" In the "assessBugType" function, there are three parameters: bugFolder, 
codeSample, and style. The function initializes a boolean variable "prune" to False and an empty string variable "bugTypeMessage". 
It gets a list of Python files in the specified "bugFolder" using the "glob" method and imports the modules from each file. 
It then executes a "detect" function from each module to detect any bugs in the "codeSample". 
If a bug is detected, "prune" is set to True, and the "bugTypeMessage" is updated.
"""


def assessBugType(bugFolder: str, codeSample, style: threadingStyle):
    prune = False
    bugTypeMessage = ""
    bugDirectoryHandle = Path(__file__).parent.glob("**/*.py")
    bugFiles = [os.path.basename(bugFile) for bugFile in bugDirectoryHandle]

    for bugFile in bugFiles:
        if bugFile == "__init__.py" or bugFile == "probe.py":
            continue
        prober = importlib.import_module(
            bugFolder + "." + bugFile[:-3], "../" + bugFolder + "/" + bugFile
        )
        bugDetector = getattr(prober, "detect" + bugFile[:-3])
        status, bugTypeMessage = bugDetector(codeSample)
        if status == True:
            prune = True
            break
    return prune, bugTypeMessage