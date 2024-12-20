'''
The following code-pair does not contain an IncorrectInit bug.
'''

buggyCode = '''
qc = QuantumCircuit(2)
qc.x(1)
qc.draw()
'''

patchedCode = '''
qc = QuantumCircuit(2)
qc.h(1)
qc.draw()
'''