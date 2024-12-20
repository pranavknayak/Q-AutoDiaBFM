'''
The following code-pair does not contain an IncorrectRegister bug.
'''

buggyCode = '''
qreg = QuantumRegister(3)
circ = QuantumCircuit(qreg, 3)
circ.y(0)
circ.cx(0, 1)
circ.cx(1, 2)
circ.measure([0,1,2], [0,1,2])
'''

patchedCode = '''
qreg = QuantumRegister(3)
creg = ClassicalRegister(3)
circ = QuantumCircuit(qreg, creg)
circ.y(0)
circ.cx(0, 1)
circ.cx(1, 2)
circ.measure([0,1,2], [0,1,2])
'''
