'''
The following code-pair does not contain an ExcessiveMeasurement bug.
'''

buggyCode = '''
qc = QuantumCircuit(2, 2)
for i in range(9):
  qc.measure(0, 0)
qc.measure(0, 0)
'''

patchedCode = '''
qc = QuantumCircuit(2, 2)
for i in range(10):
  qc.measure(0, 0)
'''
