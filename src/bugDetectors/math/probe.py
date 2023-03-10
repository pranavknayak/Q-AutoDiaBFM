from bugInvestigator import threadingStyle
import importlib
import os
from pathlib import Path
import random
import threading


def assessBugClass(editScript):
    prune = True
    # Add in the pakad here
    return prune

def assessBugType(bugFolder: str, editScript, style: threadingStyle):
    prune = False
    bugTypeMessage = ""
    bugDirectoryHandle = Path(__file__).parent.glob('**/*.py')
    bugFiles = [os.path.basename(bugFile) for bugFile in bugDirectoryHandle]
    # shouldThread = True

    # if style == threadingStyle.nil:
    #     shouldThread = False
    # elif style == threadingStyle.random:
    #     if random.rangerange(0, 2, 1) == 0: 
    #         shouldThread = False
    #     else: 
    #         shouldThread = True

    for bugFile in bugFiles: # Thread it as appropriate
        if bugFile == '__init__.py' or bugFile == 'probe.py': continue
        prober = importlib.import_module(bugFolder + "." + bugFile[:-3], 
                                         "../" + bugFolder + "/" + bugFile)
        bugDetector = getattr(prober, "detect" + bugFile[:-3])
        status, bugTypeMessage = bugDetector(editScript)
        if status == True:
            prune = True
            break
    return prune, bugTypeMessage