'''
The following code-pair contains an IncorrectInit bug.
'''

buggyCode = '''
qc = QuantumCircuit(3)
qc.h(0)
qc.x(0 + 1)
qc.draw()
'''

patchedCode = '''
qc = QuantumCircuit(3)
qc.h(0)
qc.x(1 + 1)
qc.draw()
'''