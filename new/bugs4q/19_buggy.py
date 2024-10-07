from qiskit import *
from qiskit.aqua.circuits import FourierTransformCircuits as QFT

circuit = QuantumCircuit(3)
circuit.initialize( psi, [i for i in reversed(circuit.qubits)])

QFT.construct_circuit(circuit=circuit, qubits=circuit.qubits[:2], inverse=True)

backend = Aer.get_backend('statevector_simulator')
final_state = execute(circuit, backend, shots=1).result().get_statevector()
