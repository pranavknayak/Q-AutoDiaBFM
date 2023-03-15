'''
The following code-pair does not contain an IncorrectMeasurement bug.
'''

buggyCode = '''
qc = QuantumCircuit(2)
qc.x(0)
qc.h(0)
qc.measure(0, 0)
'''

patchedCode = '''
qc = QuantumCircuit(2)
qc.x(0)
qc.h(1)
qc.measure(0, 0)
'''