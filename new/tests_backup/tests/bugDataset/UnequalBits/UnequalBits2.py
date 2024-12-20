'''
The following code-pair does not contain an IncorrectRegister bug.
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
circuit = QuantumCircuit(3, 2)
circuit.x(0)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.measure([0,1,2], [0,1,2])
'''
