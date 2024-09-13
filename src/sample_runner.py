"""This code imports a module named "bugInvestigator" with an alias "bI".
It then calls the function "classifyBugs" from the module with three arguments and prints the returned message to the console.
"""
import bugInvestigator as bI
import os


# buggyCode = """
# import math
# from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
#
# def circuit_aperiod15(qc,qr,cr,a):
#     if a == 11:
#         circuit_11period15(qc,qr,cr)
#         return
#
#     qc.x(qr[0])
#
#     qc.h(qr[4])
#     qc.h(qr[4])
#     qc.measure(qr[4],cr[0])
#     qc.reset(qr[4])
#
#     qc.h(qr[4])
#     qc.cx(qr[2],qr[2])  # Changed from qc.cx(qr[4],qr[2])
#     qc.cx(qr[4],qr[0])
#     qc.p(math.pi/2.,qr[4]).c_if(cr, 1)
#     qc.h(qr[4])
#     qc.measure(qr[4],cr[1])
#     qc.reset(qr[4])
#
#     qc.h(qr[4])
#     circuit_amod15(qc,qr,cr,a)
#     qc.p(3.*math.pi/4.,qr[4]).c_if(cr, 3)
#     qc.p(math.pi/2.,qr[4]).c_if(cr, 2)
#     qc.p(math.pi/4.,qr[4]).c_if(cr, 1)
#     qc.h(qr[4])
#     qc.measure(qr[4],cr[2])
#
# q = QuantumRegister(5)
# c = ClassicalRegister(5)
# shor = QuantumCircuit(q,c)
#
# circuit_aperiod15(shor,q,c, 7)
# print(shor.draw())
# """
#
# fixedCode = """
# import math
# from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
#
# def circuit_aperiod15(qc,qr,cr,a):
#     if a == 11:
#         circuit_11period15(qc,qr,cr)
#         return
#
#     qc.x(qr[0])
#
#     qc.h(qr[4])
#     qc.h(qr[4])
#     qc.measure(qr[4],cr[0])
#     qc.reset(qr[4])
#
#     qc.h(qr[4])
#     qc.cx(qr[4],qr[2])
#     qc.cx(qr[4],qr[0])
#     qc.p(math.pi/2.,qr[4]).c_if(cr, 1)
#     qc.h(qr[4])
#     qc.measure(qr[4],cr[1])
#     qc.reset(qr[4])
#
#     qc.h(qr[4])
#     circuit_amod15(qc,qr,cr,a)
#     qc.p(3.*math.pi/4.,qr[4]).c_if(cr, 3)
#     qc.p(math.pi/2.,qr[4]).c_if(cr, 2)
#     qc.p(math.pi/4.,qr[4]).c_if(cr, 1)
#     qc.h(qr[4])
#     qc.measure(qr[4],cr[2])
#
# q = QuantumRegister(5)
# c = ClassicalRegister(5)
# shor = QuantumCircuit(q,c)
#
# circuit_aperiod15(shor,q,c, 7)
# print(shor.draw())
# """

i = 12

if i < 10:
  bugfile = f"./bugs4q/0{i}_buggy.py"
  fixedfile = f"./bugs4q/0{i}_fixed.py"
else:
  bugfile = f"./bugs4q/{i}_buggy.py"
  fixedfile = f"./bugs4q/{i}_fixed.py"
if os.path.isfile(bugfile) and os.path.isfile(fixedfile):
  buggyCode = open(bugfile, "r").read()
  fixedCode = open(fixedfile, "r").read()


bugErrorMessage = bI.classifyBugs(buggy=buggyCode, patched=fixedCode, commandLine=False)





# Should return incorrectGate and incorrectInit

"""
Pattern one-hot vector:
[
 incorrect_init,
 incorrect_registers,
 incorrect_measurement,
 excessive_measurement,
 incorrect_standard_gate,
 incorrect_opaque_gate,
 unclosed_hadamard
]
"""
