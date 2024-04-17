"""This code imports a module named "bugInvestigator" with an alias "bI".
It then calls the function "classifyBugs" from the module with three arguments and prints the returned message to the console.
"""
import bugInvestigator as bI
import os
import traceback

i = 12


if i < 10:
  bugfile = f"./Q-PAC/Bugs4Q/0{i}_buggy.py"
  fixedfile = f"./Q-PAC/Bugs4Q/0{i}_fixed.py"
else:
  bugfile = f"./Q-PAC/Bugs4Q/{i}_buggy.py"
  fixedfile = f"./Q-PAC/Bugs4Q/{i}_fixed.py"
if os.path.isfile(bugfile) and os.path.isfile(fixedfile):
  buggyCode = open(bugfile, "r").read()
  fixedCode = open(fixedfile, "r").read()

bugErrorMessage = bI.classifyBugs(buggy=buggyCode, patched=fixedCode, commandLine=False)





# Should return incorrectGate and incorrectInit

"""
Pattern one-hot vector:
[
 incorrect_init,
 incorrect_registers,
 incorrect_measurement,
 excessive_measurement,
 incorrect_standard_gate,
 incorrect_opaque_gate,
 unclosed_hadamard
]
"""
