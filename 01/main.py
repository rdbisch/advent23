import sys

def calibrate(line):
    minIdx, maxIdx = None, None
    for i, c in enumerate(line):
        if c in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if (minIdx == None): minIdx = int(c)
            maxIdx = int(c)
    return (minIdx, maxIdx)

def toDigit(calibrate_tuple):
    if (calibrate_tuple[0] is None) or (calibrate_tuple[1] is None): return 0
    return 10*int(calibrate_tuple[0]) + int(calibrate_tuple[1])

if __name__ == "__main__":
    ctotal = 0
    for line in sys.stdin:
        ctotal += toDigit(calibrate(line))

    print(ctotal)
       
        
