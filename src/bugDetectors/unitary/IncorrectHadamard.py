import ast
import re
import numpy as np

def extractIters(node: ast.For):
    target = ast.Name(node.target)
    target_id = target.id
    if isinstance(node.iter, ast.Call):
        return  ast.Constant(node.iter.args[0]).value
    elif isinstance(node.iter, ast.List):
        return len(node.iter.elts)

def checkHadamard(codeDiff, astSample):
    qubitRegex = "\.h\(.*\)"
    circuitRegex = ".+\.h"

    buggy, patched = codeDiff[0], codeDiff[1]
    buggyID, patchedID = {}, {}
    buggyList = list(filter(("").__ne__, buggy.split("\n")))
    patchedList = list(filter(("").__ne__, patched.split("\n")))

    buggyAST, patchedAST = ast.walk(astSample[0]), ast.walk(astSample[1])

    for node in buggyAST:
        if isinstance(node, ast.Assign):
            for id in getattr(node, "targets"):
                if (
                    id.id not in buggyID
                    and isinstance(node.value, ast.Call)
                    and getattr(node, "value").func.id == "QuantumCircuit"
                ):
                    args = node.value.args
                    assert isinstance(args[0], ast.Constant), f"TODO: Hadamard detector can't handle circuits initialized with registers"
                    qubits = args[0].value
                    buggyID[id.id] = [0] * qubits

    for node in patchedAST:
        if isinstance(node, ast.Assign):
            for id in getattr(node, "targets"):
                if (
                    id.id not in patchedID
                    and isinstance(node.value, ast.Call)
                    and getattr(node, "value").func.id == "QuantumCircuit"
                ):
                    args = node.value.args
                    assert isinstance(args[0], ast.Constant), f"TODO: Hadamard detector can't handle circuits initialized with registers"
                    qubits = args[0].value
                    patchedID[id.id] = [0] * qubits

    for line in buggyList:
        qbit_result = re.search(qubitRegex, line)
        if qbit_result is None:
            continue
        qubit_id = int(qbit_result.group()[3:-1])
        circ_result = re.search(circuitRegex, line)
        circ_id = circ_result.group()[:-2]
        buggyID[circ_id][qubit_id] += 1

    for line in patchedList:
        qbit_result = re.search(qubitRegex, line)
        if qbit_result is None:
            continue
        qubit_id = int(qbit_result.group()[3:-1])
        circ_result = re.search(circuitRegex, line)
        circ_id = circ_result.group()[:-2]
        patchedID[circ_id][qubit_id] += 1

    for circ in buggyID:
      if circ in patchedID:
        for i in range(min(len(buggyID[circ]), len(patchedID[circ]))):
          if buggyID[circ][i] % 2 != 0 and patchedID[circ][i] % 2 == 0:
            return True
    return False

def detectIncorrectHadamard(codeDiff, astSample):
    status = False
    bugTypeMessage = "Unclosed Hadamard gate detected."
    status = checkHadamard(codeDiff, astSample)

    return status, bugTypeMessage
