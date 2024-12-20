'''
The following code-pair contains / does not contain an IncorrectOpaqueGate bug.
'''

buggyCode = '''
qc = QuantumCircuit(3, 3)
gt = Gate('gt', 2, [])
qc.append(gt, [0, 1])
subc = QuantumCircuit(2, name='subc')
subc.h(0)
subc.cx(0, 1)
subc.h(0)
gt2 = subc.to_instruction()
qc.append(gt2, [1, 2])
'''

patchedCode = '''
qc = QuantumCircuit(3, 3)
gt = Gate('gt', 2, [])
qc.append(gt, [0, 1])
subc = QuantumCircuit(2, name='subc')
subc.h(0)
subc.cx(0, 1)
subc.h(0)
gt2 = subc.to_instruction()
qc.append(gt2, [1, 2])
'''
