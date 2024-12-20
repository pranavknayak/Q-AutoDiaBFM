from qiskit import *
from qiskit.visualization import plot_histogram

circuit = QuantumCircuit(3, 3)

# entangle cubit 1 & 2

circuit.h(1)

circuit.cx(1, 2)

# apply CNOT to qubit we want to send
circuit.cx(0, 1)

circuit.h(0)

circuit.measure([0,1], [0,1])

circuit.cx(1, 2)

circuit.cz(0, 2)

print(circuit)

backend = Aer.get_backend('qasm_simulator')
job = execute(circuit, backend, shots=1024)
result = job.result()

counts = result.get_counts(circuit)
plot_histogram(counts)
