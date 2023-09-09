'''
The following code-pair does not contain an IncorrectRegister bug.
'''

buggyCode = '''
qc_ = QuantumCircuit(2)
qc_.h(1)
qc_.draw()

qreg = QuantumRegister(3)
circuit = QuantumCircuit(qreg, 3)
circuit.y(0)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.measure([0,1,2], [0,1,2])
'''

patchedCode = '''
qc = QuantumCircuit(2)
qc.h(1)
qc.draw()

qreg = QuantumRegister(3)
creg = ClassicalRegister(3)
circ = QuantumCircuit(qreg, creg)
circ.y(0)
circ.cx(0, 1)
circ.cx(1, 2)
circ.measure([0,1,2], [0,1,2])
'''