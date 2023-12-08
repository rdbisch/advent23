import sys
import numpy as np

if __name__ == "__main__":
    result = 0
    
    for line in sys.stdin:
        line = line.strip()
        winners = set(line.split("|")[0].split(' '))
        numbers = set(line.split("|")[1].split(' '))
        if '' in winners: winners.remove('')
        if '' in numbers: numbers.remove('')
        inter = winners.intersection(numbers)
        print(f"{line} {winners} {numbers} {inter}")
        if len(inter) > 0:
            result += np.power(2, len(inter) - 1)

    print(result)