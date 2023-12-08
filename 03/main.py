import sys

digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

def anySymbol(substr):
    valid = "*$=#/%&+-@"
    return any(v in substr for v in valid)

# Returns a list of all adjacent symbols and their indices.
# x= and y= are added to the indicdes if provided
def allSymbols(substr, x=0, y=0):
    valid = "*$=#/%&+-@"
    results = []
    for i, s in enumerate(substr):
        for v in valid:
            if s == v: results.append((x + i, y))
    
    return results      

def product(numbers):
    if (len(numbers) == 1): return numbers[0]
    else: return numbers[0] * product(numbers[1:])

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
    coord_dict = {}

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
        
        # PART 1
        #if line > 0 and anySymbol( lines[line - 1][startR:endR] ): foundSymbol = True
        #if (not foundSymbol) and line + 1 < len(lines) and anySymbol( lines[line + 1][startR:endR] ): foundSymbol = True
        #if (not foundSymbol and start > 0) and anySymbol( lines[line][start - 1] ): foundSymbol = True
        #if (not foundSymbol and end < len(lines[0])) and anySymbol( lines[line][end] ): foundSymbol = True

        # PART2
        matching_coords = []
        if line > 0: matching_coords += allSymbols(lines[line - 1][startR:endR], x=startR, y=line-1 )
        if line + 1 < len(lines): matching_coords += allSymbols( lines[line + 1][startR:endR], x=startR, y=line+1 )
        if (start > 0): matching_coords += allSymbols( lines[line][start - 1], x=start-1, y=line )
        if (end < len(lines[0])): matching_coords += allSymbols( lines[line][end], x=end, y=line )

        print(matching_coords)
        for coord in matching_coords:
            print(coord)
            if coord in coord_dict: coord_dict[coord].append(number)
            else: coord_dict[coord] = [number]

        #if (foundSymbol): sum_partnos += number
        #else:
        #    print(f"Number @ line {line} start {start} end {end} number {number} had no symbol.")

    print(coord_dict)
    for coord, numbers in coord_dict.items():
        if (lines[coord[1]][coord[0]] == '*') and len(numbers) > 1: sum_partnos += product(numbers)

    print(sum_partnos)