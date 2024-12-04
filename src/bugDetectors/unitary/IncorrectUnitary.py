
import re
import numpy as np
import ast

def is_unitary(matrix, tol=1e-10):
    """
    Check if a matrix is unitary.

    Parameters:
    matrix (numpy.ndarray): The matrix to check.
    tol (float): Tolerance for numerical errors.

    Returns:
    bool: True if the matrix is unitary, False otherwise.
    """
    identity = np.eye(matrix.shape[0])
    unitary_check = np.allclose(matrix.conj().T @ matrix, identity, atol=tol)
    return unitary_check

def extract_arrays(code):
    """
    Extract arrays defined in the code.

    Parameters:
    code (str): The code string to parse.

    Returns:
    dict: A dictionary mapping variable names to numpy arrays.
    """
    # Pattern to match variable assignments like variable = np.array([...])
    pattern = r'(\w+)\s*=\s*np\.array\(([\s\S]*?)\)'
    matches = re.findall(pattern, code)
    arrays = {}
    for var, arr_str in matches:
        try:
            # Safely evaluate the array string to a Python object
            arr = ast.literal_eval(arr_str)
            arrays[var] = np.array(arr)
        except:
            pass  # Ignore if the array cannot be parsed
    return arrays

def identify_non_unitary_arrays(correct_code, buggy_code):
    """
    Identify arrays in the buggy code that lead to non-unitary matrices.

    Parameters:
    correct_code (str): The correct Python (Qiskit) code.
    buggy_code (str): The buggy Python (Qiskit) code.

    Returns:
    list: A list of variable names that lead to non-unitary matrices.
    """
    correct_arrays = extract_arrays(correct_code)
    buggy_arrays = extract_arrays(buggy_code)
    non_unitary_arrays = []
    for var in buggy_arrays:
        if var in correct_arrays:
            buggy_arr = buggy_arrays[var]
            correct_arr = correct_arrays[var]
            if not np.array_equal(buggy_arr, correct_arr):
                if not is_unitary(buggy_arr):
                    non_unitary_arrays.append(var)
        else:
            # Optionally check arrays not present in the correct code
            buggy_arr = buggy_arrays[var]
            if not is_unitary(buggy_arr):
                non_unitary_arrays.append(var)
    return non_unitary_arrays

# Example usage:
correct_code = '''
import numpy as np
A = np.array([[0, 1],
              [1, 0]])
B = np.array([[0, -1j],
              [1j, 0]])
'''

buggy_code = '''
import numpy as np
A = np.array([[1, 0],
              [0, 1]])
B = np.array([[1, 2],
              [3, 4]])
C = np.array([[0, -1],
              [1, 0]])
'''

non_unitary_vars = identify_non_unitary_arrays(correct_code, buggy_code)
print("Arrays leading to non-unitary matrices:", non_unitary_vars)
