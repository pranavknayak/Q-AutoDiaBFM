#This code imports four modules and defines a function named "assessBugClass" that takes three arguments and returns a tuple of two values. 
#The function searches for a bug in subdirectories of a given folder and assesses the type of bug if found by importing and executing 
#a module named "probe".

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
