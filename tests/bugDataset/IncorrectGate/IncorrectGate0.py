buggyCode = '''
a = QuantumCircuit(2)
a.sdg(1)
a.draw()
'''

patchedCode = '''
qc = QuantumCircuit(2)
qc.tdg(1)
qc.draw()
'''