import sys
import numpy as np

def differences(vec):
    n = len(vec)
    if n > 0:
        return vec[1:n] - vec[0:(n-1)]
    else:
        return np.array([])
    
def applyDifferences(vec):
    d = []
    d.append(vec)
    next = vec
    while len(next) > 0 and not np.all(next == 0):
        next = differences(d[-1])
        d.append(next)
    return d

def projectArray(array1, array2):
    ret = np.pad(array2, (0, 1))
    ret[-1] = array2[-1] + array1[-1]
    return ret

def projectArrays(arrays):
    for i in range(len(arrays) - 1):
        last = len(arrays) - 1 - i
        next = last - 1
        ret = projectArray(arrays[last], arrays[next])
        arrays[next] = ret
    return arrays[0][-1]

def projectArrays_s2(arrays):
    new_arrays = []

    ######### 5 10 13 16 21 30
    #         5 3  3  5  9
    #        -2 0 2 4 6
    #         2 2 2 2 2 
    #         0 0 0 0 0

    #         x0 0 0 0 0 0    st. x = 0 since i = 0
    #         x1 2 2 2 2 2 2  st. (2 - x1) = x0 => x1 = 2 - x0
    #         x2 -2 0 2 4 6   st. (-2 - x2) = x1 => x2 = -2 - x1
    #
    for i, ar in enumerate(reversed(arrays)):
        na = np.pad(ar, (1, 0))
        if  i == 0: na[0] = 0
        else: na[0] = ar[0] - new_arrays[-1][0]

        new_arrays.append(na)
    print(new_arrays)
    return new_arrays[-1][0]

if __name__ == "__main__":
    s = 0
    for line in sys.stdin:
        digits = np.array(line.strip().split(' '), dtype='int64')
        print(applyDifferences(digits))
        x = projectArrays_s2(applyDifferences(digits))
        print(f"digits={digits} => {x}")
        s += x 

    print(s)