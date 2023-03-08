# compare the diff lines
# note that there are only a finite number of inbuilt gates in qiskit
# provided the identifier is the same, check if the other files' gate matches with an inbuilt gate.
# incase it is a custom made gate, think
import ast


def detectIncorrectGate(editScript):
    status = True
    bugTypeMessage = "Incorrect gate(s) used."

    return status, bugTypeMessage