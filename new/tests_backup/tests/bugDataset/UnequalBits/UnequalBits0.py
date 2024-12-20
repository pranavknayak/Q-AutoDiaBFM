#TODO: Clean up all 6 examples
'''
The following code-pair contains an IncorrectRegister bug.
'''

buggyCode = '''
qreg = QuantumRegister(3)
creg = ClassicalRegister(2)
circuit = QuantumCircuit(qreg, creg)
circuit.y(0)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.measure([0,1,2], [0,1,2])
'''

patchedCode = '''
qreg = QuantumRegister(3)
creg = ClassicalRegister(3)
circuit = QuantumCircuit(qreg, creg)
circuit.y(0)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.measure([0,1,2], [0,1,2])
'''
