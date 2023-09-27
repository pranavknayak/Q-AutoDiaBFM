"""This code imports a module named "bugInvestigator" with an alias "bI".
It then calls the function "classifyBugs" from the module with three arguments and prints the returned message to the console.
"""
import bugInvestigator as bI


buggyCode = '''
qc = QuantumCircuit(2, 2)
for i in range(10):
  qc.measure(0, 0)
qc.measure(1, 1)
'''

patchedCode = '''
qc = QuantumCircuit(2, 2)
for i in range(5):
  qc.measure(0, 0)
qc.measure(1, 0)
'''

# Should return incorrectGate and incorrectInit

bugErrorMessage = bI.classifyBugs(buggy=buggyCode, patched=patchedCode, commandLine=False)
print(bugErrorMessage)
