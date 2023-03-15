# compare the diff lines
# note that there are only a finite number of inbuilt gates in qiskit
# provided the identifier is the same, check if the other files' gate matches with an inbuilt gate.
# incase it is a custom made gate, think
import ast
import re

def measurementTimingError(codeSamole):

    return False

def measurementRegisterError(codeSample):
    availableMeasurementFunctions = ['measure', 'measure_all', 'measure_inactive']
    regexPattern = ""

    if len(codeSample[1]) == 1:
        editScriptStringed = str(codeSample[1])[2:-2]
        temporaryStatus = re.search(regexPattern, editScriptStringed)
        if temporaryStatus is not None:
            buggyFunctionIdentifier = editScriptStringed.split()
            patchedFunctionIdentifier = editScriptStringed.split()
            if (buggyFunctionIdentifier not in availableMeasurementFunctions) or (patchedFunctionIdentifier not in availableMeasurementFunctions):
                return False
            # either it is something like 
    else:
        return False
            
    return True



def detectIncorrectMeasurement(codeSample):
    status = False
    bugTypeMessage = "Measurement(s) performed incorrectly."
    

    # again done only with a quantum circuit object.
    # 1. If the arguments are not matching then something is off.
    # 2. Or if it is measured in the wrong place in the code. Not hhandling right now?



    return status, bugTypeMessage
