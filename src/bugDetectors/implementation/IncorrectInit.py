# compare the diff lines
# note that there are only a finite number of inbuilt gates in qiskit
# provided the identifier is the same, check if the other files' gate matches with an inbuilt gate.
# incase it is a custom made gate, think
import ast


def detectIncorrectInit(editScript):
    status = False
    bugTypeMessage = "Incorrect initialization(s) attempted."

    # Identify variables being initialized in the script
    variables = []
    for line in editScript.split('\n'):
        if '=' in line:
            variable_name = line.split('=')[0].strip()
            variables.append(variable_name)

    # Check each variable initialization for correctness
    for variable in variables:
        try:
            exec(editScript)
            exec(f"type({variable})") # Check the data type of the variable
        except:
            # If the variable is not initialized correctly, set status and update bugTypeMessage
            status = True
            bugTypeMessage = f"Incorrect initialization(s) attempted for variable {variable}."
            break
    

    return status, bugTypeMessage
