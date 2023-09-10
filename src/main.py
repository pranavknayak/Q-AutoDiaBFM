"""This code imports a module named "bugInvestigator" with an alias "bI".
It then calls the function "classifyBugs" from the module with three arguments and prints the returned message to the console.
"""
import bugInvestigator as bI


buggyCode = '''
creg = ClassicalRegister(5)
qreg = QuantumRegister(6)
qc = QuantumCircuit(creg, qreg)
'''

patchedCode = '''
creg1 = ClassicalRegister(5)
qreg = QuantumRegister(5)
qc = QuantumCircuit(creg1, qreg)
'''

# Should return incorrectGate and incorrectInit

bugErrorMessage = bI.classifyBugs(buggy=buggyCode, patched=patchedCode, commandLine=False)
print(bugErrorMessage)
