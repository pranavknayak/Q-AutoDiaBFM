'''
The following code-pair does not contain an IncorrectMeasurement bug.
'''

buggyCode = '''
qc = QuantumCircuit(3, 3)
qc.h(0)
qc.x(range(3))
qc.measure([0,1], [0, 1])
'''

patchedCode = '''
q = QuantumCircuit(3, 3)
q.h(0)
q.x(range(3))
q.measure([0,1], [0, 1])
'''