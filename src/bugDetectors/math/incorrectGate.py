# compare the diff lines
# note that there are only a finite number of inbuilt gates in qiskit
# provided the identifier is the same, check if the other files' gate matches with an inbuilt gate.
# incase it is a custom made gate, think
import ast
import re


def singleLineInbuiltGateError(codeSample):
    availableInbuiltGates = ['cx', 'h', 'i', 'p', 's', 'sdg', 't', 'tdg', 'u', 'x', 'y', 'z']
    regexPattern = " *Update\(\(identifier:.+, *line [0-9]+:[0-9] - [0-9]+:[0-9]\), .+\) *"

    if len(codeSample[1]) == 1:
        editScriptStringed = str(codeSample[1])[2:-2]
        print(editScriptStringed)
        temporaryStatus = re.search(regexPattern, editScriptStringed)
        if temporaryStatus is not None:
            buggyGate = editScriptStringed.split("((identifier:")[1].split(",")[0]
            patchedGate = editScriptStringed.split("), ")[1].split(")")[0]
            if (buggyGate not in availableInbuiltGates) or (patchedGate not in availableInbuiltGates) or (buggyGate == patchedGate):
                return False
            # how to check if identifier is a qc
        else:
            return False
    else:
        return False
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
    status |= singleLineInbuiltGateError(codeSample)

    return status, bugTypeMessage