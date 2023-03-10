# compare the diff lines
# note that there are only a finite number of inbuilt gates in qiskit
# provided the identifier is the same, check if the other files' gate matches with an inbuilt gate.
# incase it is a custom made gate, think
import ast


def detectQubitCount(editScript):
    status = False
    bugTypeMessage = "Incorrect number of qubits used."

    return status, bugTypeMessage