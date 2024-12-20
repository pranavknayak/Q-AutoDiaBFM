import qiskit
from qiskit import QuantumRegister, QuantumCircuit

qreg = QuantumRegister(1)
circuit = QuantumCircuit(qreg)

circuit._qubits = []
circuit.qregs = []

circuit.add_register(qreg)

print(circuit.qregs)
print(circuit.qubits)
