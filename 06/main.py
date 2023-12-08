import sys
import numpy as np

def toIntList(alist):
    return [ int(el) for el in alist if el != '' ]

if __name__ == "__main__":
    time = None
    distance = None

    for line in sys.stdin:
        parse = line.strip().split(':')[1].strip().split(' ')
        if time == None: time = toIntList(parse)
        else: distance = toIntList(parse)

    results = 1
    for i in range(len(time)):
        t = time[i]
        d = distance[i]

        # Let v be the duration the button is pressed.  
        # The interval is (0, v) (v, t)
        # The distance covered in the interval (v, t) is v*(t - v)
        #   =  - v^2 + vt
        #  
        # We wish to find the interval V, v in V, that satisfies 
        #  - v^2 + vt > d
        #
        #  - v^2 + vt - d > 0
        #  - v^2 + vt - d == 0
        #  v = [ -t +/- SQRT[ t^2 - 4(-1)(-d) ] ] / -2
        #    = 0.5t -/+ SQRT[ t^2 - 4d ]
        discriminant = np.sqrt( t*t - 4*d )
        lower = 0.5 * (t - discriminant)
        upper = 0.5 * (t + discriminant)


        # if either the lower or upper is exactly zero on the integer
        #  we have to bump it up one since it doesn't techincally break the record!
        # Ok, part 2 numbers are so big that isclose is failing and incorrectly shrinking the interval.
        #  So we will have to test it another way.  
        lower_i = np.ceil(lower)
        if np.isclose(lower, lower_i, rtol=1e-10): lower_i = lower_i + 1
        upper_i = np.floor(upper)
        if np.isclose(upper, upper_i, rtol=1e-10): upper_i = upper_i - 1

        size = upper_i - lower_i + 1
        print(f"t={t} d={d} discriminant={discriminant} lower={lower} upper={upper} loweri={lower_i} upper_i={upper_i} size={size}")
        results *=size 
    print(results)