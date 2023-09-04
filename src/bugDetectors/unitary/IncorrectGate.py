import ast
import re


def inbuiltGateError(codeSample):
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
    regexPattern = ".+\..*"

    buggy, patched = codeSample[0], codeSample[1]
    buggyID, patchedID = {}, {}
    buggyList = list(filter(("").__ne__, buggy.split("\n")))
    patchedList = list(filter(("").__ne__, patched.split("\n")))
    buggyGate, patchedGate = [], []
    astBuggy, astPatched = ast.walk(ast.parse(buggy)), ast.walk(ast.parse(patched))

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

    """ Checks if the gate is amongst the available gates in Qiskit."""
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

    """ Checks if the number of gates used in both codes are the same."""
    if len(buggyGate) != len(patchedGate):
        return False

    """ Checks if any of the gates used are differenet, line by line in both the codes."""
    for index in range(len(buggyGate)):
        if buggyGate[index] != patchedGate[index]:
            return True

    return False

def customGateError(codeSample):
    buggy, patched = codeSample[0], codeSample[1]
    buggyList = list(filter(("").__ne__, buggy.split("\n")))
    patchedList = list(filter(("").__ne__, patched.split("\n")))
    astBuggy, astPatched = ast.walk(ast.parse(buggy)), ast.walk(ast.parse(patched))
    buggyGateIDs = {}
    buggyCustomIDs = {}

    for node in astBuggy:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            for target in node.targets:
                if (target.id not in buggyGateIDs 
                        and isinstance(node.value.func, ast.Name) 
                        and node.value.func.id == 'Gate'):
                    gate = node.value
                    for argument in gate.args:
                        if isinstance(argument, ast.Constant) and argument.value > 2:
                            buggyGateIDs[target.id] = []
                            break
                    for kwargument in gate.keywords:
                        if kwargument.arg == 'num_qubits' and kwargument.value.value > 2:
                            buggyGateIDs[target.id] = []
                            break

                if (target.id not in buggyCustomIDs
                        and isinstance(node.value.func, ast.Attribute)
                        and node.value.func.attr == 'to_instruction'):
                    buggyCustomIDs[target.id] = []

                


    patchedGateIDs = {}
    patchedCustomIDs = {}
    for node in astPatched:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            for target in node.targets:
                if (target.id not in patchedGateIDs 
                        and isinstance(node.value.func, ast.Name) 
                        and node.value.func.id == 'Gate'):
                    gate = node.value
                    for argument in gate.args:
                        if isinstance(argument, ast.Constant) and argument.value > 2:
                            patchedGateIDs[target.id] = []
                            break
                    for kwargument in gate.keywords:
                        if kwargument.arg == 'num_qubits' and kwargument.value.value > 2:
                            patchedGateIDs[target.id] = []
                            break

                if (target.id not in patchedCustomIDs
                        and isinstance(node.value.func, ast.Attribute)
                        and node.value.func.attr == 'to_instruction'):
                    patchedCustomIDs[target.id] = []

    buggyGateCount, buggyCustomCount = len(buggyGateIDs), len(buggyCustomIDs)
    patchedGateCount, patchedCustomCount = len(patchedGateIDs), len(patchedCustomIDs)

    if buggyGateCount > patchedGateCount:
        opaqueGateReduction = buggyGateCount - patchedGateCount
        compositeGateIncrease = patchedCustomCount - buggyCustomCount
        if opaqueGateReduction <= compositeGateIncrease:
            return True

    return False


def detectIncorrectGate(codeSample):
    status = False
    bugTypeMessage = "Incorrect usage of gate(s)."
    status |= inbuiltGateError(codeSample) | customGateError(codeSample)

    return status, bugTypeMessage
