# compare the diff lines
# note that there are only a finite number of inbuilt gates in qiskit
# provided the identifier is the same, check if the other files' gate matches with an inbuilt gate.
# incase it is a custom made gate, think
import ast
import re


def inbuiltGateError(codeSample):
    availableInbuiltGates = ['ccx', 'cx', 'h', 'i', 'p', 's', 'sdg', 't', 'tdg', 'u', 'x', 'y', 'z']
    regexPattern = " *Update\(\(identifier:.+, *line [0-9]+:[0-9] - [0-9]+:[0-9]\), .+\) *"
    buggy, patched = codeSample[0], codeSample[2]
    buggyList, patchedList = buggy.split('\n'), patched.split('\n')
    modify = ""
    for j in buggyList:
        modify += j + "\n"
    print(modify)
    buggyID, patchedID = {}, {}

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

    #print(codeSample[1])

    if len(buggyID) == 0 or len(buggyID) != len(patchedID):
        return False

    if len(codeSample[1]) == 1:
        editScriptStringed = str(codeSample[1])[2:-2]
        temporaryStatus = re.search(regexPattern, editScriptStringed)
        if temporaryStatus is not None:
            buggyGate = editScriptStringed.split("((identifier:")[1].split(",")[0]
            patchedGate = editScriptStringed.split("), ")[1].split(")")[0]
            if (buggyGate not in availableInbuiltGates) or (patchedGate not in availableInbuiltGates) or (buggyGate == patchedGate):
                return False
            
                 
        else:
            return False
    else:
        return False

    # if len(codeSample[1]) == 1:
    #     editScriptStringed = str(codeSample[1])[2:-2]
    #     temporaryStatus = re.search(regexPattern, editScriptStringed)
    #     if temporaryStatus is not None:
    #         buggyGate = editScriptStringed.split("((identifier:")[1].split(",")[0]
    #         patchedGate = editScriptStringed.split("), ")[1].split(")")[0]
    #         if (buggyGate not in availableInbuiltGates) or (patchedGate not in availableInbuiltGates) or (buggyGate == patchedGate):
    #             return False
            
            
    #     else:
    #         return False
    # else:
    #     return False

    return True


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
