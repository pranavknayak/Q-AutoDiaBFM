'''
The following code-pair does not contain an IncorrectRegister bug.
'''

buggyCode = '''
qc = QuantumCircuit(3, 3)
qc.h(0)
qc.x(range(3))
qc.measure([0,1], [0, 1])
'''

patchedCode = '''
qc = QuantumCircuit(3, 3)
qc.h(0)
qc.x(range(3))
qc.measure([0,1], [1, 0])
'''