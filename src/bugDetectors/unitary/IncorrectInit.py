import ast
import numpy as np
import re


def returnArgs(args):
    args = "".join(args.split(" "))
    square = []
    paren = []  
    value = ""
    parenCheck = 0
    squareCheck = 0

    for char in args:
        if char == '(':
            parenCheck = 1
        elif char == '[':
            squareCheck = 1
        elif char == ']':
            squareCheck = 0
            square.append(value)
            paren.append(square)
            square = []
            value = ""
        elif char == ')':
            parenCheck = 0
            if len(value) > 0:
                paren.append(value)
        elif char == ',':
            if parenCheck and value != "":
                if squareCheck:
                    square.append(value)
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

def checkIncorrectParam(codeSample): 
    regex1 = ".+\..*"
    regex2 = ".+QuantumCircuit.*"
    availableInbuiltGates = ['ccx', 'cx', 'h', 'i', 'p', 's', 'sdg', 't', 'tdg', 'u', 'x', 'y', 'z']

    buggy, patched = codeSample[0], codeSample[2]
    buggyID, patchedID = {}, {}
    buggyList = list(filter(("").__ne__, buggy.split("\n")))
    patchedList = list(filter(("").__ne__, patched.split("\n")))
    buggyGate, patchedGate = {}, {}
    buggyQuantum, patchedQuantum = {}, {}
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
    
    if len(buggyID) != len(patchedID):
        return False

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
    
    buggyGateValue, patchedGateValue = list(buggyGate.values()), list(patchedGate.values())
    buggyQuantumValue, patchedQuantumValue = list(buggyQuantum.values()), list(patchedQuantum.values()) 

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


def detectIncorrectInit(codeDiff):
    status = False
    bugTypeMessage = "Incorrect initialization(s) attempted."
    status = checkIncorrectParam(codeDiff)
    
    return status, bugTypeMessage
