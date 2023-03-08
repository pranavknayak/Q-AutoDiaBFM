import bugInvestigator as bI

bugErrorMessage = bI.classifyBugs(buggy = "test0", patched = "test1", commandLine = False)
print(bugErrorMessage)