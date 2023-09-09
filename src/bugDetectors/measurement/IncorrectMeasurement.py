import ast
import numpy as np
import re

#TODO: Add more iteration options (dictionaries and list comprehensions)
def extractIters(node: ast.For):
    target = ast.Name(node.target)
    target_id = target.id
    if isinstance(node.iter, ast.Call):
        return  ast.Constant(node.iter.args[0]).value
    elif isinstance(node.iter, ast.List):
        return len(node.iter.elts)


def returnArgs(args):
    args = "".join(args.split(" "))
    square = []
    paren = []
    value = ""
    parenCheck = 0
    squareCheck = 0

    for char in args:
        if char == "(":
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
            parenCheck = 0
            if len(value) > 0:
                paren.append(value)
        elif char == ",":
            if parenCheck and value != "":
                if squareCheck:
                    square.append(value)
                else:
                    paren.append(value)
        else:
            value = ""
            value += char

    for args in range(len(paren)):
        if isinstance(paren[args], list):
            for index in range(len(paren[args])):
                paren[args][index] = eval(paren[args][index])
        else:
            paren[args] = eval(paren[args])

    return np.array(paren)


def measurementRegisterError(codeSample, astSample):
    availableMeasurementFunctions = ["measure", "measure_all", "measure_inactive"]
    regexPattern = ".+\.measure.*"
    buggy, patched = codeSample[0], codeSample[1]
    buggyMeasures, patchedMeasures = {}, {}
    buggyMeasure, patchedMeasure = {}, {}
    buggyList = list(filter(("").__ne__, buggy.split("\n")))
    patchedList = list(filter(("").__ne__, patched.split("\n")))
    buggyLine, patchedLine = {}, {}
    buggyArgs, patchedArgs = [], []
    # astBuggy, astPatched = ast.walk(ast.parse(buggy)), ast.walk(ast.parse(patched))
    astBuggy, astPatched = ast.walk(astSample[0]), ast.walk(astSample[1])

    """ Deduce if there is a Quantum Circuit object associated with the patch."""
    for node in astBuggy:
        if isinstance(node, ast.Assign):
            for id in getattr(node, "targets"):
                if (
                    id.id not in buggyMeasures
                    and getattr(node, "value").func.id == "QuantumCircuit"
                ):
                    buggyMeasures[id.id] = []

        """ Using the AST to deduce if there is measure function amongst the aforementioned types."""
        if isinstance(node, ast.Expr):
            if getattr(node, "value").func.attr in availableMeasurementFunctions:
                if getattr(node, "value").func.value.id not in buggyMeasure:
                    buggyMeasure[getattr(node, "value").func.value.id] = []
                    getattr(node, "value").func.attr
                    buggyMeasure[getattr(node, "value").func.value.id].append(
                    )
                else:
                    buggyMeasure[getattr(node, "value").func.value.id].append(
                        getattr(node, "value").func.attr
                    )

    """ Same checks as above but in the patched code instead of the buggy code."""
    for node in astPatched:
        if isinstance(node, ast.Assign):
            for id in getattr(node, "targets"):
                if (
                    id.id not in patchedMeasures
                    and getattr(node, "value").func.id == "QuantumCircuit"
                ):
                    patchedMeasures[id.id] = []

        if isinstance(node, ast.Expr):
            if getattr(node, "value").func.attr in availableMeasurementFunctions:
                if getattr(node, "value").func.value.id not in patchedMeasure:
                    patchedMeasure[getattr(node, "value").func.value.id] = []
                    patchedMeasure[getattr(node, "value").func.value.id].append(
                        getattr(node, "value").func.attr
                    )
                else:
                    patchedMeasure[getattr(node, "value").func.value.id].append(
                        getattr(node, "value").func.attr
                    )

    """ Considering the cases when there is a one to one mapping of the QuantumCircuits
    in buggy code to the QuantumCircuits in patched code. """

    if len(buggyMeasures) != len(patchedMeasures):
        return False

    """ Assuming the existence of a singleton Quantum Circuit object,
        deduces if the number of instances of a measurement function
        is equal in both codes."""
    if len(buggyMeasure) != len(patchedMeasure):
        return True

    """ Deduce whether the exact same measure functions are being used in both codes."""
    buggyKeys, patchedKeys = list(buggyMeasure.keys()), list(patchedMeasure.keys())

    for i in range(len(buggyKeys)):
        if buggyMeasure[buggyKeys[i]] != patchedMeasure[patchedKeys[i]]:
            return True

    for line in range(len(buggyList)):
        tempStatus = re.search(regexPattern, buggyList[line])
        if tempStatus is not None:
            buggyLine[buggyList[line].split("measure")[1]] = line

    for line in range(len(patchedList)):
        tempStatus = re.search(regexPattern, patchedList[line])
        if tempStatus is not None:
            patchedLine[patchedList[line].split("measure")[1]] = line

    for buggyKey in buggyLine.keys():
        buggyArgs.append(returnArgs(buggyKey))

    for patchedKey in patchedLine.keys():
        patchedArgs.append(returnArgs(patchedKey))

    if len(buggyArgs) != len(patchedArgs):
        return False

    for i in range(len(buggyArgs)):
        if buggyArgs[i].shape != patchedArgs[i].shape:
            return True
        else:
            if np.array_equal(buggyArgs[i], patchedArgs[i]) == 0:
                return True

    buggyLineNum = list(buggyLine.values())
    patchedLineNum = list(patchedLine.values())

    """ Optional: can be used to print the exact line numbers of the patch."""
    # print(buggy, patched, sep = "\n***\n")
    # print(buggyLineNum, patchedLineNum)

    for num in range(len(buggyLineNum)):
        if buggyLineNum[num] != patchedLineNum[num]:
            return True

    return False

def repeatedMeasurementError(codeSample, astSample):
    availableMeasurementFunctions = ["measure", "measure_all", "measure_inactive"]
    regexPattern = ".+\.measure.*"

    buggy, patched = codeSample[0], codeSample[1]
    buggyMeasures, patchedMeasures = {}, {}
    astBuggy, astPatched = ast.walk(astSample[0]), ast.walk(astSample[1])

    for node in astBuggy:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            for target in node.targets:
                if (target.id not in buggyMeasures
                        and isinstance(node.value.func, ast.Name)
                        and node.value.func.id == 'QuantumCircuit'):
                    buggyMeasures[target.id] = 0

    for node in astPatched:
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            for target in node.targets:
                if (target.id not in patchedMeasures
                        and isinstance(node.value.func, ast.Name)
                        and node.value.func.id == 'QuantumCircuit'):
                    patchedMeasures[target.id] = 0




    astBuggy, astPatched = ast.walk(ast.parse(buggy)), ast.walk(ast.parse(patched))
    buggyCircIDs, patchedCircIDs = buggyMeasures.keys(), patchedMeasures.keys()

    for node in astBuggy:
        if isinstance(node, ast.For):
            iterations = extractIters(node)
            if not iterations:
                continue
            else:
                for subnode in node.body:
                    if isinstance(subnode, ast.Expr) and isinstance(subnode.value, ast.Call):
                        id = subnode.value.func.value.id
                        func = subnode.value.func.attr
                        if id in buggyMeasures.keys() and func in availableMeasurementFunctions:
                            buggyMeasures[id] += iterations - 1
        else:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                id = node.value.func.value.id
                func = node.value.func.attr
                if id in buggyMeasures.keys() and func in availableMeasurementFunctions:
                    buggyMeasures[id] += 1


    for node in astPatched:
        if isinstance(node, ast.For):
            iterations = extractIters(node)
            if not iterations:
                continue
            else:
                for subnode in node.body:
                    if isinstance(subnode, ast.Expr) and isinstance(subnode.value, ast.Call):
                        id = subnode.value.func.value.id
                        func = subnode.value.func.attr
                        if id in patchedMeasures.keys() and func in availableMeasurementFunctions:
                            patchedMeasures[id] += iterations - 1
        else:
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                id = node.value.func.value.id
                func = node.value.func.attr
                if id in patchedMeasures.keys() and func in availableMeasurementFunctions:
                    patchedMeasures[id] += 1

    for id in buggyCircIDs:
        if id in patchedCircIDs:
            if buggyMeasures[id] > patchedMeasures[id]:
                return True

    return False


def detectIncorrectMeasurement(codeSample, astSample):
    status = False
    bugTypeMessage = "Measurement(s) performed incorrectly."
    status = measurementRegisterError(codeSample, astSample) | repeatedMeasurementError(codeSample, astSample)

    return status, bugTypeMessage
