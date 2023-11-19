'''
The following code-pair does not contain an IncorrectHadamards bug.
'''

buggyCode = '''
qc = QuantumCircuit(2)
qc.h(0)
qc.cx(0,1)

'''

patchedCode = '''
qc = QuantumCircuit(2)
qc.h(1)
qc.cx(0,1)
'''
