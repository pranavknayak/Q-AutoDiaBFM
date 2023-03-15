#This is basically the buggy code and patched Code
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