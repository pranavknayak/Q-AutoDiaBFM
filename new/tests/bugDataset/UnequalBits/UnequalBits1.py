'''
The following code-pair contains an IncorrectRegister bug.
'''

buggyCode = '''
circuit = QuantumCircuit(3, 2)
circuit.y(0)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.measure([0,1,2], [0,1,1])
'''

patchedCode = '''
circuit = QuantumCircuit(3, 3)
circuit.y(0)
circuit.cx(0, 1)
circuit.cx(1, 2)
circuit.measure([0,1,2], [0,1,2])
'''
