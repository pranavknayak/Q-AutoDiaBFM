'''
The following code-pair contains an IncorrectOpaqueGate bug.
'''

buggyCode = '''
qc = QuantumCircuit(3, 3)
gt = Gate('gt', 3, []) 
qc.append(gt, [0, 1, 2])
'''

patchedCode = '''
qc = QuantumCircuit(3, 3)
sub_circuit = QuantumCircuit(3, name='sub_circuit')
# Intermediate logic
gt = sub_circuit.to_instruction()
qc.append(gt, [0, 1, 2])
'''
