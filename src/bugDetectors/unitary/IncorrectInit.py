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

    buggy, patched = codeSample[0], codeSample[1]
    buggyID, patchedID = {}, {}
    buggyList = list(filter(("").__ne__, buggy.split("\n")))
    patchedList = list(filter(("").__ne__, patched.split("\n")))
    buggyGate, patchedGate = {}, {}
    buggyQuantum, patchedQuantum = {}, {}
    astBuggy, astPatched = ast.walk(ast.parse(buggy)), ast.walk(ast.parse(patched))

    ''' Retrieves all instances of a QuantumCircuit object in both, the buggy and patched codes.'''
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

    ''' Checks if the arguments are amongst the possible arguments for an inbuilt 
        gate operation in Qiskit, in both codes.
    '''
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
    
    ''' Checks if the arguments are amongst the possible arguments for a QuantumCircuit
        object in both codes.
    '''
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

    for index in range(len(buggyQuantumValue)):
        if buggyQuantumValue[index].shape != patchedQuantumValue[index].shape:
            return True
        else:
            if np.array_equal(buggyQuantumValue[index], patchedQuantumValue[index]) == 0:
                return True
    
    for index in range(len(buggyGateValue)):
        if buggyGateValue[index].shape != patchedGateValue[index].shape:
            return True
        else:
            if np.array_equal(buggyGateValue[index], patchedGateValue[index]) == 0:
                return True
        
    return False


def detectIncorrectInit(codeDiff):
    status = False
    bugTypeMessage = "Incorrect initialization(s) attempted."
    status = checkIncorrectParam(codeDiff)
    
    return status, bugTypeMessage
