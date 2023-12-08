import sys

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def anySymbol(substr):
    valid = "*$=#/%&+-@"
    return any(v in substr for v in valid)

if __name__ == "__main__":
    lines = []
    for line in sys.stdin:
        lines.append(line.strip())

    results = []
    for i, la in enumerate(lines):
        j = 0
        while j < len(la):
            el = la[j]
            if el in digits: 
                # Find extent of the number.
                k = j + 1
                while k < len(la) and la[k] in digits:
                    k = k + 1
                number = la[j:k]
                results.append({"number": number, "lineno": i, "start": j, "end": k})
                j = k
            else: 
                j = j + 1
                pass

    # For each digit ensure there is a symbol around it on the grid somewhere
    sum_partnos = 0
    for r in results:
        line = r["lineno"]
        start = r["start"]
        end = r["end"]
        number = int(r["number"])

        if start > 0: startR = start - 1
        else: startR = start

        if end < len(lines[0]): endR = end + 1
        else: endR = end

        foundSymbol = False
        
        if line > 0 and anySymbol( lines[line - 1][startR:endR] ): foundSymbol = True
        if (not foundSymbol) and line + 1 < len(lines) and anySymbol( lines[line + 1][startR:endR] ): foundSymbol = True
        if (not foundSymbol and start > 0) and anySymbol( lines[line][start - 1] ): foundSymbol = True
        if (not foundSymbol and end < len(lines[0])) and anySymbol( lines[line][end] ): foundSymbol = True

        if (foundSymbol): sum_partnos += number
        else:
            print(f"Number @ line {line} start {start} end {end} number {number} had no symbol.")


    print(sum_partnos)