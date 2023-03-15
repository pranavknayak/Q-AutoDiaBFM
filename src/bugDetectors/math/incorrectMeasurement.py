# compare the diff lines
# note that there are only a finite number of inbuilt gates in qiskit
# provided the identifier is the same, check if the other files' gate matches with an inbuilt gate.
# incase it is a custom made gate, think
import ast


def detectIncorrectMeasurement(codeSample):
    status = False
    bugTypeMessage = "Measurement(s) performed incorrectly."
    availableMeasurementFunctions = ['measure', 'measure_all', 'measure_inactive']

    # again done only with a quantum circuit object.
    # 1. If the arguments are not matching then something is off.
    # 2. Or if it is measured in the wrong place in the code. Not hhandling right now?



    return status, bugTypeMessage