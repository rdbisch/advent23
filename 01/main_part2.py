import sys

# This doens't work as it replaces later numbers first when they come alphabetically.
# Soooooo...
def expand(line):
    keys = { 
        "one": "1",
        "two": "2",
        "three": "3", 
        "four": "4",
        "five": "5",
        "six": "6",
        "seven":"7", 
        "eight": "8",
        "nine": "9" }

    for k, v in keys.items():
        line = line.replace(k, v)
    return line


def expand2(line):
    result_line = ""
    keys3 = {"one":'1', "two":'2', "six":'6'}
    keys4 = {"four":'4', "five":'5', "nine":'9'}
    keys5 = {"three":'3', "seven":'7', "eight":'8'}

    i = 0
    while (i < len(line)):
        line3 = line[i : (i + 3)]
        line4 = line[i : (i + 4)]
        line5 = line[i : (i + 5)]
        if line3 in keys3:
            result_line += keys3[line3]
        elif line4 in keys4:
            result_line += keys4[line4]
        elif line5 in keys5:
            result_line += keys5[line5]
        else:
            result_line += line[i]
        i = i + 1
    return result_line

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
        line = line.strip()
        orig_sub = toDigit(calibrate(line))
        corr_sub = toDigit(calibrate(expand2(line)))
        if orig_sub != corr_sub:
            print(f"line={line} orig={orig_sub} corr={corr_sub}")
        ctotal += corr_sub

    print(ctotal)
       
        
