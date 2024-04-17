"""This code imports a module named "bugInvestigator" with an alias "bI".
It then calls the function "classifyBugs" from the module with three arguments and prints the returned message to the console.
"""
import bugInvestigator as bI
import os
import traceback

bug_vector = [0,
              0,
              0,
              0,
              0,
              0,
              0]

for i in range(1, 65):

  if i < 10:
    bugfile = f"./Q-PAC/Bugs4Q/0{i}_buggy.py"
    fixedfile = f"./Q-PAC/Bugs4Q/0{i}_fixed.py"
    if i == 6:
      continue
  else:
    bugfile = f"./Q-PAC/Bugs4Q/{i}_buggy.py"
    fixedfile = f"./Q-PAC/Bugs4Q/{i}_fixed.py"
  if os.path.isfile(bugfile) and os.path.isfile(fixedfile):

    buggyCode = open(bugfile, "r").read()
    fixedCode = open(fixedfile, "r").read()
    try:
      bugErrorMessage = bI.classifyBugs(buggy=buggyCode, patched=fixedCode, commandLine=False)
    except BaseException as e:
      print(f"ERROR AT PAIR {i}")
      continue
      # print(traceback.format_exc(e))
    if len(bugErrorMessage['unitary']) != 0:
      if "Incorrect usage of built-in gate(s) and Incorrect usage of opaque gate(s)." in bugErrorMessage['unitary']:
        bug_vector[4] += 1
        bug_vector[5] += 1
      elif "Incorrect usage of built-in gate(s)." in bugErrorMessage['unitary']:
        bug_vector[4] += 1
      elif "Incorrect usage of opaque gate(s)." in bugErrorMessage['unitary']:
        bug_vector[5] += 1

      if "Unclosed Hadamard gate detected." in bugErrorMessage['unitary']:
        bug_vector[6] += 1

    if len(bugErrorMessage['measurement']) != 0:
      if "Measurement(s) performed incorrectly and Excessive measurements performed." in bugErrorMessage['measurement']:
        bug_vector[2] += 1
        bug_vector[3] += 1
      elif "Measurement(s) performed incorrectly." in bugErrorMessage['measurement']:
        bug_vector[2] += 1
      elif "Excessive measurements performed." in bugErrorMessage['measurement']:
        bug_vector[3] += 1

    if len(bugErrorMessage['initialization']) != 0:
      if "Incorrect initialization(s) attempted." in bugErrorMessage['initialization']:
        bug_vector[0] += 1
      if "Unequal bits vs. qubits during QuantumCircuit initialization(s)." in bugErrorMessage['initialization']:
        bug_vector[1] += 1

print(bug_vector)




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
