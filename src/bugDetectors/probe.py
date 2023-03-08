from bugInvestigator import threadingStyle
import importlib
import os
from pathlib import Path
import threading

bugPruningFileName = "probe"

def assessBugType(bugFolder: str, editScript, style: threadingStyle):
    prune = False
    _bugPackage_ = ""
    bugTypeMessage = ""
    bugDirectoryHandle = Path(__file__).parent.resolve()
    bugDirectories = [bugDirectory for bugDirectory in bugDirectoryHandle.iterdir() if bugDirectory.is_dir()]

    for bugDirectory in bugDirectories: # To be threaded as appropriate
        bugPackage = os.path.basename(bugDirectory)
        bugPackage = str(bugPackage)
        if bugPackage == "__pycache__": continue
        prober = importlib.import_module(bugFolder + "." + bugPackage + "." + bugPruningFileName, 
                                         "../" + bugPackage + "/" + bugPruningFileName + ".py")
        if prober.assessBugClass(editScript) == True:
            _bugPackage_ = bugPackage
            prune = True
            break

    if prune == True:
        prober = importlib.import_module(bugFolder + "." + _bugPackage_ + "." + bugPruningFileName, 
                                       "../" + _bugPackage_ + "/" + bugPruningFileName + ".py")
        _, bugTypeMessage = prober.assessBugType(bugFolder + "." + _bugPackage_, editScript, style)
    return prune, bugTypeMessage