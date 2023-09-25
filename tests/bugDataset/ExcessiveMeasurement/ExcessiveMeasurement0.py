'''
The following code-pair contains an ExcessiveMeasurement bug.
'''

buggyCode = '''
qc = QuantumCircuit(2, 2)
for i in range(10):
  qc.measure(0, 0)

'''

patchedCode = '''
qc = QuantumCircuit(2, 2)
for i in range(5):
  qc.measure(0, 0)
'''
