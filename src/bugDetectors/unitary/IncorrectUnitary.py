import numpy as np

def isUnitary(matrix, tol=1e-10):
    """
    Check if a matrix is unitary.

    Parameters:
    matrix (numpy.ndarray): The matrix to check.
    tol (float): Tolerance for numerical errors.

    Returns:
    bool: True if the matrix is unitary, False otherwise.
    """
    if matrix.shape[0] != matrix.shape[1]:
        return False
    identity = np.eye(matrix.shape[0])
    unitaryCheck = np.allclose(matrix.conj().T @ matrix, identity, atol=tol)
    return unitaryCheck

def extractArraysFromCode(code):
    """
    Execute code in a controlled environment and extract arrays.

    Parameters:
    code (str): The code string to execute.

    Returns:
    dict: A dictionary mapping variable names to numpy arrays.
    """
    arrays = {}
    variables = {}
    # Controlled execution environment
    safeGlobals = {'__builtins__': None, 'np': np}
    try:
        exec(code, safeGlobals, variables)
        # Recursively extract arrays from variables
        for varName, value in variables.items():
            foundArrays = extractArraysFromObject(value, varName)
            arrays.update(foundArrays)
    except Exception as e:
        print(f"Error executing code: {e}")
    return arrays

def extractArraysFromObject(obj, name):
    """
    Recursively extract arrays from an object (dicts, lists, numpy arrays).

    Parameters:
    obj: The object to search.
    name: The name of the variable or key.

    Returns:
    dict: A dictionary mapping variable names to numpy arrays.
    """
    arrays = {}
    if isinstance(obj, np.ndarray):
        arrays[name] = obj
    elif isinstance(obj, dict):
        for key, value in obj.items():
            keyName = f"{name}['{key}']"
            arrays.update(extractArraysFromObject(value, keyName))
    elif isinstance(obj, list):
        for idx, item in enumerate(obj):
            idxName = f"{name}[{idx}]"
            arrays.update(extractArraysFromObject(item, idxName))
    return arrays

def identifyNonUnitaryArrays(correctCode, buggyCode):
    """
    Identify arrays that are unitary in the correct code but not unitary in the buggy code.

    Parameters:
    correctCode (str): The correct Python code.
    buggyCode (str): The buggy Python code.

    Returns:
    list: A list of variable names that lead to non-unitary matrices.
    """
    correctArrays = extractArraysFromCode(correctCode)
    buggyArrays = extractArraysFromCode(buggyCode)
    nonUnitaryArrays = []
    for varName, correctArr in correctArrays.items():
        if isinstance(correctArr, np.ndarray):
            # Check if the array is unitary in the correct code
            if isUnitary(correctArr):
                # Check if the corresponding array exists in the buggy code
                if varName in buggyArrays:
                    buggyArr = buggyArrays[varName]
                    if isinstance(buggyArr, np.ndarray):
                        # Check if the buggy array is not unitary
                        if not isUnitary(buggyArr):
                            nonUnitaryArrays.append(varName)
    return nonUnitaryArrays

def detectIncorrectUnitary(codeDiff, astSample):
    status = identifyNonUnitaryArrays(codeDiff[1], codeDiff[0])
    if status is not None:
        status = True
    else:
        status = False
    bugTypeMessage = "Non-unitary matrix(ces) (which is/are supposed to be unitary) found."
    return status, bugTypeMessage
