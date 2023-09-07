import ast
import re

from numpy import who

def checkIncorrectRegisters(codeSample, astSample):
    
    classicalRegex = ".+ClassicalRegister.*"
    quantumRegex = ".+QuantumRegister.*"

    buggy, patched = codeSample[0], codeSample[1]
    buggyList = list(filter(("").__ne__, buggy.split("\n")))
    patchedList = list(filter(("").__ne__, patched.split("\n")))

    buggyClassicalRegisters = {}
    buggyQuantumRegisters = {}
    patchedClassicalRegisters = {}
    patchedQuantumRegisters = {}

    # astBuggy, astPatched = ast.walk(ast.parse(buggy)), ast.walk(ast.parse(patched))
    astBuggy, astPatched = astSample[0], astSample[1]

    for line in buggyList:
        temporaryStatus = re.search(classicalRegex, line)
        if temporaryStatus is not None:
            register = line.split('=')[0].strip()
            args = (line.split('ClassicalRegister')[1])
            if ',' in args:
                count = int(args[1: args.index(',')])
            else:
                count = int(args[1:-1])
            buggyClassicalRegisters[register] = count

        temporaryStatus = re.search(quantumRegex, line)
        if temporaryStatus is not None:
            register = line.split('=')[0].strip()
            args = (line.split('QuantumRegister')[1])
            if ',' in args:
                count = int(args[1: args.index(',')])
            else:
                count = int(args[1:-1])
            buggyQuantumRegisters[register] = count
            
    for line in patchedList:
        temporaryStatus = re.search(classicalRegex, line)
        if temporaryStatus is not None:
            register = line.split('=')[0].strip()
            args = (line.split('ClassicalRegister')[1])
            if ',' in args:
                count = int(args[1: args.index(',')])
            else:
                count = int(args[1:-1])
            patchedClassicalRegisters[register] = count


        temporaryStatus = re.search(quantumRegex, line)
        if temporaryStatus is not None:
            register = line.split('=')[0].strip()
            args = (line.split('QuantumRegister')[1])
            if ',' in args:
                count = int(args[1: args.index(',')])
            else:
                count = int(args[1:-1])
            patchedQuantumRegisters[register] = count

    buggyCircs = {}
    patchedCircs = {}

    for node in astBuggy:
        registerFound = 0
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            funcCall = node.value
            if funcCall.func.id == 'QuantumCircuit':
                circ = node.targets[0].id
                if circ not in buggyCircs:
                    buggyCircs[circ] = {'qubits': 0, 'bits': 0}
                for arg in funcCall.args:
                    if isinstance(arg, ast.Name) and arg.id in buggyClassicalRegisters:
                        buggyCircs[circ]['bits'] += buggyClassicalRegisters[arg.id]
                        registerFound = 1
                    if isinstance(arg, ast.Name) and arg.id in buggyQuantumRegisters:
                        buggyCircs[circ]['qubits'] += buggyQuantumRegisters[arg.id]
                        registerFound = 1

                if registerFound == 0:
                    if isinstance(funcCall.args[0], ast.Constant):
                        buggyCircs[circ]['qubits'] += funcCall.args[0].value
                        buggyCircs[circ]['bits'] += funcCall.args[1].value


    for node in astPatched:
        registerFound = 0
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
            funcCall = node.value
            if funcCall.func.id == 'QuantumCircuit':
                circ = node.targets[0].id
                if circ not in patchedCircs:
                    patchedCircs[circ] = {'qubits': 0, 'bits': 0}
                for arg in funcCall.args:
                    if isinstance(arg, ast.Name) and arg.id in patchedClassicalRegisters:
                        patchedCircs[circ]['bits'] += patchedClassicalRegisters[arg.id]
                        registerFound = 1
                    if isinstance(arg, ast.Name) and arg.id in patchedQuantumRegisters:
                        patchedCircs[circ]['qubits'] += patchedQuantumRegisters[arg.id]
                        registerFound = 1
    
                if registerFound == 0:
                    if isinstance(funcCall.args[0], ast.Constant):
                        patchedCircs[circ]['qubits'] += funcCall.args[0].value
                        patchedCircs[circ]['bits'] += funcCall.args[1].value

    for circuit in buggyCircs:
        if circuit in patchedCircs:
            if buggyCircs[circuit]['bits'] != buggyCircs[circuit]['qubits'] and patchedCircs[circuit]['bits'] == patchedCircs[circuit]['qubits']:
                return True
    return False

def detectIncorrectRegisters(codeDiff, astSample):
    status = False
    bugTypeMessage = "Unequal bits vs. qubits during QuantumCircuit initialization(s)."
    status = checkIncorrectRegisters(codeDiff, astSample)

    return status, bugTypeMessage
