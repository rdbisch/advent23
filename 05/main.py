import sys

# Using maps provided using the (to, from, length)  format
# assumes list is sorted in from order
# e.g. alist[0][from] < alist[1][from] < ... 
def mapRangeLookup(alist, ex):
    for _to, _from, _len in alist:
        if (ex >= _from and ex < _from + _len):
            return _to + (ex - _from)
    return ex

if __name__ == "__main__":

    state = 0
    maps = {}
    
    for line in sys.stdin:
        line = line.strip()

        if state == 0:
            if line[0:5] == "seeds":
                seeds = line.split(":")[1].strip().split(' ')
                print(seeds)
                state = 1
            else:
                raise RuntimeError(f"Invalid input {line} for state {state}")
            
        elif state == 1:
            if line == "":
                state = 2
            else:
                raise RuntimeError(f"Invalid input {line} for state {state}")
        
        elif state == 2:
            if line[-4:] == "map:":
                map_name = line.split(' ')[0]
                maps[map_name] = []
                state = 3
            else:
                raise RuntimeError(f"Invalid input {line} for state {state}")

        elif state == 3:
            if line != "": maps[map_name].append(line)
            elif line == "":
                state = 2
            else:
                raise RuntimeError(f"Invalid input {line} for state {state}")
            
        else:
            raise RuntimeError("invalid state {state}")
        
    # process maps
    # this works well for ordinary integers but of course the problem gives you 15 digit ranges
    #final_maps = {}
    #for map, lines in maps.items():
    #    map_result = {}
    #    for map_line in lines:
    #        t = map_line.split(' ')
    #        _to, _from, _length = int(t[0]), int(t[1]), int(t[2])
    #        print(f"{_from}, {_to}, {_length}")
    #        for i in range(_length):
    #            map_result[i + _from] = _to + i
    #    final_maps[map] = map_result

    # process maps try2
    final_maps = {}
    for map, lines in maps.items():
        new_lines = []
        for map_line in lines:
            t = map_line.split(' ')
            _to, _from, _length = int(t[0]), int(t[1]), int(t[2])
            new_lines.append((_to, _from, _length))
        new_lines = sorted(new_lines, key = lambda x: x[1])
        final_maps[map] = new_lines

    lowest = None
    lowest_seed = None
    for seed in seeds:
        x = int(seed)
        print(f"processing {x}")
        for map in ["seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water", "water-to-light", "light-to-temperature", "temperature-to-humidity", "humidity-to-location"]:            
            #y = final_maps[map].get(x, x)  # default to x=>x if the key doesn't exist
            y = mapRangeLookup(final_maps[map], x)
            print(f"map {map} {x} => {y}")
            x = y

        if lowest is None or x < lowest:
            lowest = x
            lowest_seed = seed

    print(f"{lowest} {lowest_seed}")

