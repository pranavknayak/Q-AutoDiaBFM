'''
The following code-pair contains an IncorrectMeasurement bug.
'''

buggyCode = '''
qc = QuantumCircuit(3, 3)
qc.h(0)
qc.x(range(3))
qc.measure([1,2], [0, 1])
'''

patchedCode = '''
qc = QuantumCircuit(3, 3)
qc.h(0)
qc.x(range(3))
qc.measure_all()
'''