#This code imports a module named "bugInvestigator" with an alias "bI". 
#It then calls the function "classifyBugs" from the module with three arguments and prints the returned message to the console.
import bugInvestigator as bI

bugErrorMessage = bI.classifyBugs(buggy = "test0", patched = "test1", commandLine = False)
print(bugErrorMessage)
