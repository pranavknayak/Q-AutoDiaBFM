#This is basically the buggy code and patched Code used to check the Bug Pattern
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
