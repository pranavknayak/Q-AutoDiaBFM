'''
The following code-pair does not contain an IncorrectGate bug.
'''

buggyCode = '''
a = QuantumCircuit(2)
a.x(1)
a.draw()
'''

patchedCode = '''
qc = QuantumCircuit(2)
qc.x(1)
qc.draw()
'''