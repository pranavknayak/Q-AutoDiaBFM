# TODO: Fix bug where detector returns true when only the qubit corresponding to the hadamard changes (FAILTEST: IncorrectInit0)
import ast
import re
import numpy as np

    


def extractIters(node: ast.For):
    target = ast.Name(node.target)
    target_id = target.id
    if isinstance(node.iter, ast.Call):
        return ast.Constant(node.iter.args[0]).value
    elif isinstance(node.iter, ast.List):
        return len(node.iter.elts)


def checkHadamard(codeDiff, astSample):
    qubitRegex = r"\.h\(.*\)"
    circuitRegex = r".+\.h"

    buggy_int_vals, patched_int_vals = {}, {}  # stores integers and literals

    buggy, patched = codeDiff[0], codeDiff[1]
    buggyID, patchedID = {}, {}
    buggyRegs, patchedRegs = (
        {},
        {},
    )  # Keeps track of register names and bit counts, for initializing circuits
    buggyList = list(filter(("").__ne__, buggy.split("\n")))
    patchedList = list(filter(("").__ne__, patched.split("\n")))

    containsHadamard = 0
    for line in buggyList:
        present = re.search(qubitRegex, line)
        if present is not None:
            containsHadamard += 1
    if containsHadamard == 0:
        return False

    buggyAST, patchedAST = ast.walk(astSample[0]), ast.walk(astSample[1])

    for node in buggyAST:
        if isinstance(node, ast.Assign):
            for id in getattr(node, "targets"):
                if isinstance(node.value, ast.Constant):
                    buggy_int_vals[id.id] = node.value.value
                elif (
                    id.id not in buggyID
                    and isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Name)
                    and getattr(node, "value").func.id == "QuantumCircuit"
                ):
                    qubits = 0
                    args = node.value.args
                    if isinstance(args[0], ast.Constant):
                        qubits = args[0].value
                    elif isinstance(args[0], ast.Name):
                        if args[0].id in buggyRegs:
                            qubits = buggyRegs[args[0].id]
                        elif args[0].id in buggy_int_vals:
                            qubits = buggy_int_vals[args[0].id]
                    buggyID[id.id] = [0] * qubits
                elif (
                    id.id not in buggyRegs
                    and isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Name)
                    and node.value.func.id == "QuantumRegister"
                ):
                    if isinstance(node.value.args[0], ast.Name):
                        buggyRegs[id.id] = buggy_int_vals[node.value.args[0].id]
                    else:
                        buggyRegs[id.id] = node.value.args[0].value

    for node in patchedAST:
        if isinstance(node, ast.Assign):
            for id in getattr(node, "targets"):
                if isinstance(node.value, ast.Constant):
                    patched_int_vals[id.id] = node.value.value
                elif (
                    id.id not in patchedID
                    and isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Name)
                    and getattr(node, "value").func.id
                    == "QuantumCircuit"  # Throwing bug, investigate further.
                ):
                    qubits = 0
                    args = node.value.args
                    if isinstance(args[0], ast.Constant):
                        qubits = args[0].value
                    elif isinstance(args[0], ast.Name):
                        if args[0].id in patchedRegs:
                            qubits = patchedRegs[args[0].id]
                        elif args[0].id in patched_int_vals:
                            qubits = patched_int_vals[args[0].id]

                    patchedID[id.id] = [0] * qubits
                elif (
                    id.id not in patchedRegs
                    and isinstance(node.value, ast.Call)
                    and isinstance(node.value.func, ast.Name)
                    and node.value.func.id == "QuantumRegister"
                ):
                    if isinstance(node.value.args[0], ast.Name):
                        patchedRegs[id.id] = patched_int_vals[node.value.args[0].id]
                    else:
                        patchedRegs[id.id] = node.value.args[0].value

    for line in buggyList:
        qbit_result = re.search(qubitRegex, line)
        full_reg = False
        if qbit_result is None:
            continue
        qubit_id = qbit_result.group()[3:-1]
        if qubit_id.isnumeric():
            qubit_id = int(qubit_id)
        else:
            sqb_pattern = r"\[.*\]"
            if re.search(sqb_pattern, qubit_id) is None:
                full_reg = True
            else:
                id1 = qubit_id.find("[")
                id2 = qubit_id.rfind("]")
                qubit_id = int(qubit_id[id1 + 1 : id2])
        circ_result = re.search(circuitRegex, line)
        circ_id = circ_result.group()[:-2].strip()
        if full_reg:
            for i in range(len(buggyID[circ_id])):
                buggyID[circ_id][i] += 1
        else:
            buggyID[circ_id][qubit_id] += 1

    for line in patchedList:
        qbit_result = re.search(qubitRegex, line)
        full_reg = False
        if qbit_result is None:
            continue
        qubit_id = qbit_result.group()[3:-1]
        if qubit_id.isnumeric():
            qubit_id = int(qubit_id)
        else:
            sqb_pattern = r"\[.*\]"
            if re.search(sqb_pattern, qubit_id) is None:
                full_reg = True
            else:
                id1 = qubit_id.find("[")
                id2 = qubit_id.rfind("]")
                qubit_id = int(qubit_id[id1 + 1 : id2])
        circ_result = re.search(circuitRegex, line)
        circ_id = circ_result.group()[:-2].strip()
        if full_reg:
            for i in range(len(patchedID[circ_id])):
                patchedID[circ_id][i] += 1
        else:
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
    try:
        status = checkHadamard(codeDiff, astSample)
        print("checkHadamard WORKS")
    except:
        status = False
        print("error in checkHadamard")
        raise

    return status, bugTypeMessage
