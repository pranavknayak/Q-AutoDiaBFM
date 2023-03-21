# compare the diff lines
# note that there are only a finite number of inbuilt gates in qiskit
# provided the identifier is the same, check if the other files' gate matches with an inbuilt gate.
# incase it is a custom made gate, think
import ast
import re

def inbuiltGateError(codeSample):
    availableInbuiltGates = ['ccx', 'cx', 'h', 'i', 'p', 's', 'sdg', 't', 'tdg', 'u', 'x', 'y', 'z']
    regexPattern = ".+\..*"

    buggy, patched = codeSample[0], codeSample[2]
    buggyID, patchedID = {}, {}
    buggyList = list(filter(("").__ne__, buggy.split("\n")))
    patchedList = list(filter(("").__ne__, patched.split("\n")))
    buggyGate, patchedGate = [], []
    astBuggy, astPatched = ast.walk(ast.parse(buggy)), ast.walk(ast.parse(patched))
    
    for node in astBuggy:
        if isinstance(node, ast.Assign):
            for id in getattr(node, 'targets'):
                if id.id not in buggyID and getattr(node, 'value').func.id == "QuantumCircuit":
                    buggyID[id.id] = []
    
    for node in astPatched:
        if isinstance(node, ast.Assign):
            for id in getattr(node, 'targets'):
                if id.id not in patchedID and getattr(node, 'value').func.id == "QuantumCircuit":
                    patchedID[id.id] = []
    
    ''' Considering the cases when there is a one to one mapping of the QuantumCircuits 
    in buggy code to the QuantumCircuits in patched code. '''

    if len(buggyID) != len(patchedID):
        return False
    
    for line in buggyList:
        temporaryStatus = re.search(regexPattern, line)
        if temporaryStatus is not None:
            iden = line.split(".")[0]
            gate = line.split(".")[1].split("(")[0]
            if iden in buggyID and gate in availableInbuiltGates:
                buggyGate.append(gate)
    
    for line in patchedList:
        temporaryStatus = re.search(regexPattern, line)
        if temporaryStatus is not None:
            iden = line.split(".")[0]
            gate = line.split(".")[1].split("(")[0]
            if iden in patchedID and gate in availableInbuiltGates:
                patchedGate.append(gate)
    
    if len(buggyGate) != len(patchedGate):
        return False

    for index in range(len(buggyGate)):
        if buggyGate[index] != patchedGate[index]:
            return True
    
    return False

def detectIncorrectGate(codeSample):
    status = False
    bugTypeMessage = "Incorrect usage of gate(s)."
    '''
    1. Inbuilt gates based errors.
        a. single line errors.
        b. multiline errors.
    2. Customised gates based errors.
    '''
    status |= inbuiltGateError(codeSample)

    return status, bugTypeMessage