import sys

# Using maps provided using the (to, from, length)  format
# assumes list is sorted in from order
# e.g. alist[0][from] < alist[1][from] < ... 
def mapRangeLookup(alist, ex):
    for _to, _from, _len in alist:
        if (ex >= _from and ex < _from + _len):
            return _to + (ex - _from)
    return ex

# If provided a key of the form (x, _, len) which corresponds to multiple keys x, x+1, ..., x + len
#  returns an exhaustive but perhaps disjoint set of output ranges:
# [(y1, x, len1), (y2, x + len1, len2), .. ]
# where len1 + len2 + ... = len
def mapRangesLookup(alist, ex, _keylength):
    print(f"mapRangesLookup alist={alist} ex={ex} _keylength={_keylength}")
    partial_results = []
    for _to, _from, _len in alist:
        # Here, ex is not a point, but an interval (ex, ex + keylength)
        #  our ultimate goal is to map this onto a new interval via the function defined in alist.
        # That function is piece series of intervals for which its mapping is valid.  
        # There are three cases to consider
        # The first is that ex is entirely contained within the interal [from, from + len].  Trivial.
        # The second is that ex is partially contained within the interval [from, from + len], thereby creating the need to splinter the interval. Hard.
        # The third is that ex is not in the interval, in which case we just move along to the next. Trivial.

        # So the second case then:
        #     Case 2.a:         ex == from < ex + keylength < from + len
        #  (Note our preconditions should make the case ex < from impossible.)
        #      So this is actually case 1.  Trivial.

        #     Case 2.b:         from < ex < from + keylength < ex + keylength
        #         create subset:   ex => (ex[0:L], , L), (ex[L:], , keylength - L)
        #                               case 1             Then we pretend that ex = ex[L:] with keylength -= L for the rest of the algorithm.  
        #                                                  we can do this because alist is also in sorted order by the interval!

        if (ex >= _from and ex < _from + _len):
            # (ex, _keylength) (_from, _len) (_to, _len)
            before_ex_len = ex - _from
                   # size of ex    # size of the subdivision (from, len) into (from, before_ex_len) + (from + before_ex_len, remaining)
            L = min( _keylength, _len - before_ex_len)
            partial_results.append((_to + before_ex_len, ex, L))
            ex = ex + L
            _keylength -= L
    
    if _keylength > 0:
        partial_results.append((ex, ex, _keylength))

    return partial_results

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
    for i, seed in enumerate(seeds):
        if (i % 2) == 1: continue
        length = int(seeds[i + 1])
        x = [(int(seed), None, length)]
        #print(f"processing {x} ")
        for map in ["seed-to-soil", "soil-to-fertilizer", "fertilizer-to-water", "water-to-light", "light-to-temperature", "temperature-to-humidity", "humidity-to-location"]:            
            #y = final_maps[map].get(x, x)  # default to x=>x if the key doesn't exist
            #y = mapRangeLookup(final_maps[map], x)
            results = []
            for r in x:
                y = mapRangesLookup(final_maps[map], r[0], r[2])
                #print(f"map {map} {r} => {y}")
                results = results + y            
            x = results
        #print(x)
        for i, (_to, _from, _len) in enumerate(results):
            if lowest is None or _to < lowest:
                lowest = _to
                lowest_seed = seed

    print(f"{lowest} {lowest_seed}")

