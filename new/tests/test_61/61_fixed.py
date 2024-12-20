import qiskit
from qiskit import QuantumRegister, QuantumCircuit
qreg = QuantumRegister(1, name="old")
circuit = QuantumCircuit(qreg)
circuit.h(qreg[0])

#print(circuit)
#        ┌───┐
# old_0: ┤ H ├
#        └───┘

circuit.transform_registers(new_qregs=[QuantumRegister(1, name="new")])

#print(circuit)
#        ┌───┐
# new_0: ┤ H ├
#        └───┘

print(circuit.qubits)
# [Qubit(QuantumRegister(1, 'new'), 0)]

print(circuit.qregs)
# [QuantumRegister(1, 'new')]
