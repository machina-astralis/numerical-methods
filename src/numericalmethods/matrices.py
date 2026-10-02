import numpy as np
class matrixresult: 
    def __init__ (self, solution, message = None):
        self.solution = solution
        self.message = message
    def __str__(self):
        return(
            f"solution = {self.solution}\n"
            f"message = {self.message}"
        )

def pivoting (arr): 
    '''parameters(1)
    arr: an n by n+1 matrix 
    functionality: preforms pivoting on a matrix to assure a diagonally dominant form 
    returns: pivoted matrix 
    '''
    for j in range (len(arr)):
        pivot = arr[j][j]
        cpi = j 
        for i in range (j, len(arr)):
            if abs(arr[i][j]) > abs(pivot):
                pivot = arr[i][j]
                cpi = i 

        arr[[cpi, j]] = arr[[j, cpi]]
    return arr


def elimination(arr):
    '''parameters (1):
arr: the n by n+1 array
functionality: impliments forward elimination in order to remove the lower triangle of values in the matrix
return: arr '''
    for j in range (len(arr)-1):
        
        for i in range (j+1, len(arr)):
            const = (arr[i][j] / arr [j][j])
            arr[i] = arr [i] - (arr[j]*const)
#             
    return arr


def backsub (arr):
    '''parameters (1):
arr: the n by n+1 array
functionality: impliments back substutiton in order to solve for unknown variables 
return: arr '''
    xterm = []
    for i in range (1, arr.shape[1], 1):
        xterm.append(f'x{i}')

    xval = np.zeros(arr.shape[0])
    
    for i in range (arr.shape[0]-1, -1, -1):
        total = arr[i][-1]
        for j in range (arr.shape[1]-2, i, -1):
            total -= (arr[i][j] * xval[j])
        xval[i] = total / arr [i][i]
    
    return xval


def gauss_elimination (arr):
    '''parameters (1):
arr: the n by n+1 array
functionality: impliments gauss elimination in order to solve for unknown variables 
returns: '''
    arr = pivoting (arr)
    arr = elimination (arr)
    for i in range (len(arr)):
        if np.all(np.abs(arr[i][:-1]) < 1e-15) and np.abs(arr[i][-1]) > 1e-15:
            return matrixresult(
                solution = None,
                message = "No solution exists"
            )
    arr = backsub(arr)
    return matrixresult(
        solution = arr,
        message = "Solution found"
    )
                