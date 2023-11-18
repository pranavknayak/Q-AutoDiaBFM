'''
The following code-pair contains an IncorrectOpaqueGate bug.
'''

buggyCode = '''
qc = QuantumCircuit(4, 4)
gt = Gate('gt', 3, []) 
gt2 = Gate('gt2', 3, []) 
qc.append(gt, [0, 1, 2])
qc.append(gt2, [1, 2, 3])
'''

patchedCode = '''
qc = QuantumCircuit(4, 4)
sub_circuit = QuantumCircuit(3, name='sub_circuit')
sub_circuit2 = QuantumCircuit(3, name='sub_circuit2')
# Intermediate logic to emulate gate behaviour by circuits
gt = sub_circuit.to_instruction()
gt2 = sub_circuit2.to_instruction()
qc.append(gt, [0, 1, 2])
qc.append(gt2, [1, 2, 3])
'''
