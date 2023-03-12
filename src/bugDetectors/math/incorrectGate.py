# compare the diff lines
# note that there are only a finite number of inbuilt gates in qiskit
# provided the identifier is the same, check if the other files' gate matches with an inbuilt gate.
# incase it is a custom made gate, think
import ast
import code_diff

def detectIncorrectGate(codeSample):
    status = False
    bugTypeMessage = "Incorrect usage of gate(s)."
    # print(type(editScript))
    # print(editScript)
    # list = [x, h, t, s, ]
    cc = code_diff.difference('''
    x = 5
    ''',
    '''
    h = 5
    ''', lang = 'python')
    print(cc.edit_script())
    return status, bugTypeMessage