#The code imports threadingStyle enum from bugInvestigator module along with necessary modules such as importlib, os, and pathlib. 
#The assessBugClass function takes bugFolder, codeSample, and style as input parameters and iterates through bug directories to import the probe module. 
#If the bug is detected, the code assesses its type and returns a prune flag and bugTypeMessage.


from bugInvestigator import threadingStyle
import importlib
import os
from pathlib import Path
import threading

bugPruningFileName = "probe"

def assessBugClass(bugFolder: str, codeSample, style: threadingStyle):
    prune = False
    _bugPackage_ = ""
    bugTypeMessage = ""
    bugDirectoryHandle = Path(__file__).parent.resolve()
    bugDirectories = [bugDirectory for bugDirectory in bugDirectoryHandle.iterdir() if bugDirectory.is_dir()]

    for bugDirectory in bugDirectories: # To be threaded as appropriate
        bugPackage = os.path.basename(bugDirectory)
        if bugPackage == "__pycache__": continue
        prober = importlib.import_module(bugFolder + "." + bugPackage + "." + bugPruningFileName, 
                                         "../" + bugPackage + "/" + bugPruningFileName + ".py")
        if prober.assessBugClass(codeSample) == True:
            _bugPackage_ = bugPackage
            prune = True
            # break
        if prune == True:
            prober = importlib.import_module(bugFolder + "." + _bugPackage_ + "." + bugPruningFileName, 
                                        "../" + _bugPackage_ + "/" + bugPruningFileName + ".py")
            status, bugTypeMessage = prober.assessBugType(bugFolder + "." + _bugPackage_, codeSample, style)
            if status == True:
                break
            else: 
                prune = False
                continue 
    return prune, bugTypeMessage
