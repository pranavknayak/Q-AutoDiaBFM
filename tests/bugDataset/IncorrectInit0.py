buggyCode = '''
qc = QuantumCircuit(2)
qc.h(0)
qc.draw()
'''

patchedCode = '''
qc = QuantumCircuit(2)
qc.h(1)
qc.draw()
'''
