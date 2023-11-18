'''
The following code-pair contains an IncorrectOpaqueGate bug.
'''

buggyCode = '''
qc = QuantumCircuit(4, 4)
gt1 = Gate('gt', 3, []) 
gt2 = Gate('gt2', 3, [])
qc.append(gt, [0, 1, 2])
qc.append(gt2, [1, 2, 3])
'''

patchedCode = '''
qc = QuantumCircuit(4, 4)
gt1 = Gate('gt1', 2, [])
gt2 = Gate('gt2', 2, [])
# Intermediate logic to emulate gate behaviour by circuits
qc.append(gt1, [0, 1])
qc.append(gt2, [1, 2])
'''
