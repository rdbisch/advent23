import sys
import numpy as np

def differences(vec):
    print(vec)
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

if __name__ == "__main__":
    s = 0
    for line in sys.stdin:
        digits = np.array(line.strip().split(' '), dtype='int64')
        print(digits)
        x = projectArrays(applyDifferences(digits))
        print(f"digits={digits} => {x}")
        s += x 

    print(s)