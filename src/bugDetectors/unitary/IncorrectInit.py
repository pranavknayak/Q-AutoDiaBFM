# compare the diff lines
# note that there are only a finite number of inbuilt gates in qiskit
# provided the identifier is the same, check if the other files' gate matches with an inbuilt gate.
# incase it is a custom made gate, think
import ast
import re
import numpy as np


def returnArgs(args):
    args = "".join(args.split(" "))
    square = []
    paren = []
    value = ""
    parenCheck = 0
    subparencheck = 0
    squareCheck = 0

    for char in args:
        if char == "(":
            if parenCheck == 1:
                subparencheck = 1
                value += char
            else:
                parenCheck = 1
        elif char == "[":
            squareCheck = 1
        elif char == "]":
            squareCheck = 0
            square.append(value)
            paren.append(square)
            square = []
            value = ""
        elif char == ")":
            if subparencheck == 1:
                subparencheck = 0
                value += char
            else:
                parenCheck = 0
                if len(value) > 0:
                    paren.append(value)
        elif char == ",":
            if parenCheck and value != "":
                if squareCheck:
                    square.append(value)
                elif subparencheck:
                    subparen += (value,)
                else:
                    paren.append(value)
            value = ""
        else:
            value += char

    for args in range(len(paren)):
        if isinstance(paren[args], list):
            for index in range(len(paren[args])):
                paren[args][index] = eval(paren[args][index])
        else:
            paren[args] = eval(paren[args])

    return np.array(paren)


def checkIncorrectParam(codeSample, astSample):
    regex1 = ".+\..*"
    regex2 = ".+QuantumCircuit.*"
    availableInbuiltGates = [
        "ccx",
        "cx",
        "h",
        "i",
        "p",
        "s",
        "sdg",
        "t",
        "tdg",
        "u",
        "x",
        "y",
        "z",
    ]

    buggy, patched = codeSample[0], codeSample[1]
    buggyID, patchedID = {}, {}
    buggyList = list(filter(("").__ne__, buggy.split("\n")))
    patchedList = list(filter(("").__ne__, patched.split("\n")))
    buggyGate, patchedGate = {}, {}
    buggyQuantum, patchedQuantum = {}, {}
    # astBuggy, astPatched = ast.walk(ast.parse(buggy)), ast.walk(ast.parse(patched))
    astBuggy, astPatched = ast.walk(astSample[0]), ast.walk(astSample[1])

    """ Retrieves all instances of a QuantumCircuit object in both, the buggy and patched codes."""
    for node in astBuggy:
        if isinstance(node, ast.Assign):
            for id in getattr(node, "targets"):
                if (
                    id.id not in buggyID
                    and getattr(node, "value").func.id == "QuantumCircuit"
                ):
                    buggyID[id.id] = []

    for node in astPatched:
        if isinstance(node, ast.Assign):
            for id in getattr(node, "targets"):
                if (
                    id.id not in patchedID
                    and getattr(node, "value").func.id == "QuantumCircuit"
                ):
                    patchedID[id.id] = []

    """ Considering the cases when there is a one to one mapping of the QuantumCircuits
    in buggy code to the QuantumCircuits in patched code. """
    if len(buggyID) != len(patchedID):
        return False

    """ Deduces if the arguments are amongst the possible arguments for an inbuilt
        gate operation in Qiskit, in both codes.
    """
    for line in buggyList:
        temporaryStatus = re.search(regex1, line)
        if temporaryStatus is not None:
            gate = line.split(".")[1].split("(")[0]
            if gate in availableInbuiltGates:
                args = line.split(gate)[1]
                if gate not in buggyGate:
                    buggyGate[gate] = returnArgs(args)

    for line in patchedList:
        temporaryStatus = re.search(regex1, line)
        if temporaryStatus is not None:
            gate = line.split(".")[1].split("(")[0]
            if gate in availableInbuiltGates:
                args = line.split(gate)[1]
                if gate not in patchedGate:
                    patchedGate[gate] = returnArgs(args)

    """ Checks if the arguments are amongst the possible arguments for a QuantumCircuit
        object in both codes.
    """
    # TODO: Check if args are ints before passing, if not then directly store the variable names
    for line in buggyList:
        temporaryStatus = re.search(regex2, line)
        if temporaryStatus is not None:
            args = line.split("QuantumCircuit")[1]
            buggyQuantum[line] = returnArgs(args)

    for line in patchedList:
        temporaryStatus = re.search(regex2, line)
        if temporaryStatus is not None:
            args = line.split("QuantumCircuit")[1]
            patchedQuantum[line] = returnArgs(args)

    buggyGateValue, patchedGateValue = list(buggyGate.values()), list(
        patchedGate.values()
    )
    buggyQuantumValue, patchedQuantumValue = list(buggyQuantum.values()), list(
        patchedQuantum.values()
    )

    # TODO: Update this logic to account for the value lists containing strings and not just ints

    for i in range(len(buggyQuantumValue)):
        if buggyQuantumValue[i].shape != patchedQuantumValue[i].shape:
            return True
        else:
            if np.array_equal(buggyQuantumValue[i], patchedQuantumValue[i]) == 0:
                return True

    for i in range(len(buggyGateValue)):
        if buggyGateValue[i].shape != patchedGateValue[i].shape:
            return True
        else:
            if np.array_equal(buggyGateValue[i], patchedGateValue[i]) == 0:
                return True

    return False


def detectIncorrectInit(codeDiff, astSample):
    status = False
    bugTypeMessage = "Incorrect initialization(s) attempted."
    status = checkIncorrectParam(codeDiff, astSample)

    return status, bugTypeMessage
