import os
import re

def read_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
def mutate(file_path):
    file = read_file(file_path)
    circuits = {}
    qregs = {}
    cregs = {}
    circuit_regex = re.compile(r'[a-zA-Z]\w* = \w*\.?QuantumCircuit\(\w*,?\s?\w*\)')
    qreg_regex = re.compile(r'[a-zA-Z]\w* = \w*\.?QuantumRegister\(\w*,?\s?\w*\)')
    creg_regex = re.compile(r'[a-zA-Z]\w* = \w*\.?ClassicalRegister\(\w*,?\s?\w*\)')

    for i in qreg_regex.findall(file):
        qreg_id = i.split('=').strip()
        qregs[qreg_id] = 0

    for i in creg_regex.findall(file):
        creg_id = i.split('=').strip()
        cregs[creg_id] = 0



    for i in circuit_regex.findall(file):
        circuit_id = i.split('=').strip()
        circuits[circuit_id] = 0
         

if __name__ == "__main__":
    mutate('./tester2.py')
