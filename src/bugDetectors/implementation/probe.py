import sys
import threading
from ..probe import threadingStyle # verify if it really works

def assessBugType(editScript, style: threadingStyle):
    prune = False
    bugType = "random"


    return prune, bugType