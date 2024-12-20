'''
The following code-pair does not contain an IncorrectGate bug.
'''

buggyCode = '''
qc = QuantumCircuit(2)
qc.x(1)
qc.draw()
'''

patchedCode = '''
qc = QuantumCircuit(2)
qc.draw()
qc.x(1)
'''