""" This code imports four modules and defines a function named "assessBugClass" that takes three arguments and returns a tuple of two values.
The function searches for a bug in subdirectories of a given folder and assesses the type of bug if found by importing and executing
a module named "probe".
"""

from bugInvestigator import threadingStyle
import importlib
import os
from pathlib import Path
import ast

bugPruningFileName = "probe"

""" Assess which bug-fix class does the bug-fix pattern belong to, at this level of the tree."""


def assessBugClass(bugFolder: str, codeSample, style: threadingStyle):
    prune = False
    _bugPackage_ = ""
    bugTypeMessage = ""
    bugDirectoryHandle = Path(__file__).parent.resolve()
    bugDirectories = [
        bugDirectory
        for bugDirectory in bugDirectoryHandle.iterdir()
        if bugDirectory.is_dir()
    ]

    buggy = codeSample[0]
    patched = codeSample[1]

    buggyAST = ast.walk(ast.parse(buggy))
    patchedAST = ast.walk(ast.parse(patched))

    astSample = (buggyAST, patchedAST)
    bugTypeMessages = {}
    """ Iterates through all available bug-fix classes at the current level."""
    for bugDirectory in bugDirectories:
        bugPackage = os.path.basename(bugDirectory)
        bugTypeMessages[bugPackage] = []
        if bugPackage == "__pycache__":
            continue
        prober = importlib.import_module(
            bugFolder + "." + bugPackage + "." + bugPruningFileName,
            "../" + bugPackage + "/" + bugPruningFileName + ".py",
        )
        """ Finds an appropriate bug-fix class."""
        if prober.assessBugClass(codeSample) == True:
            _bugPackage_ = bugPackage
            prune = True
        """ Since the current level identifies as the parent of the children of the tree,
            it iterates over the modules here to find the precise bug-fix detection motif.
            Else it would recursively go to the next level of bug-fix classes.
        """
        if prune == True:
            prober = importlib.import_module(
                bugFolder + "." + _bugPackage_ + "." + bugPruningFileName,
                "../" + _bugPackage_ + "/" + bugPruningFileName + ".py",
            )
            status, bugTypeMessage = prober.assessBugType(
                bugFolder + "." + _bugPackage_, codeSample, astSample, style
            )
            if status == True:
                bugTypeMessages[bugPackage].append(bugTypeMessage)
                continue
            else:
                prune = False
                continue
    return prune, bugTypeMessages
