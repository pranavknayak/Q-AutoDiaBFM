# compare the diff lines
# note that there are only a finite number of inbuilt gates in qiskit
# provided the identifier is the same, check if the other files' gate matches with an inbuilt gate.
# incase it is a custom made gate, think
import ast
import code_diff

def detectIncorrectGate(codeSample):
    status = False
    bugTypeMessage = "Incorrect usage of gate(s)."
    '''
    1. Inbuilt gates based errors.
        a. single line errors.
        b. multiline errors.
    2. Customised gates based errors.
    '''

    print(codeSample[1])

    # Handling 1a

    availableInbuiltGates = ['cx', 'h', 'i', 'p', 's', 'sdg', 't', 'u', 'x', 'y', 'z']




    # print(type(editScript))
    # print(editScript)
    # list = [x, h, t, s, ]
    # using b, p codes, I will check if it is of the form qc.<gate? -> qc.<another gate>

    # cc = code_diff.difference('''
    # x = 5
    # ''',
    # '''
    # h = 5
    # ''', lang = 'python')
    # print(cc.edit_script())
    return status, bugTypeMessage