import math
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister

def circuit_aperiod15(qc,qr,cr,a):
    if a == 11:
        circuit_11period15(qc,qr,cr)
        return
    
    qc.x(qr[0])

    qc.h(qr[4])
    qc.h(qr[4])
    qc.measure(qr[4],cr[0])
    qc.reset(qr[4])

    qc.h(qr[4])
    qc.cx(qr[4],qr[2])
    qc.cx(qr[4],qr[0])
    qc.p(math.pi/2.,qr[4]).c_if(cr, 1)
    qc.h(qr[4])
    qc.measure(qr[4],cr[1])
    qc.reset(qr[4])

    qc.h(qr[4])
    circuit_amod15(qc,qr,cr,a)
    qc.p(3.*math.pi/4.,qr[4]).c_if(cr, 3)
    qc.p(math.pi/2.,qr[4]).c_if(cr, 2)
    qc.p(math.pi/4.,qr[4]).c_if(cr, 1)
    qc.h(qr[4])
    qc.measure(qr[4],cr[2])

q = QuantumRegister(5)
c = ClassicalRegister(5)
shor = QuantumCircuit(q,c)

circuit_aperiod15(shor,q,c, 7)
print(shor.draw())
