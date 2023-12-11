import sys
import numpy as np

# Computes the shortest path from every point to g1
def shortestPath(g1, space_height, space_width):
    rows, cols = space_height.shape
    steps = -np.ones(space_height.shape)
    steps[g1] = 0
    
    visited = set()
    visit = set()
    visit.add(g1)

    while (len(visit) > 0):
        index = visit.pop()
        visited.add(index)
        #print(f"visiting {index} visit = {visit} visited = {visited}")

        # This is the number of steps it takes to get to index.  
        old_steps = steps[index]

        for dir, offset in [('h', (-1, 0)), ('h', (1, 0)), ('w', (0, -1)), ('w', (0, 1))]:
            new_index = (index[0]+offset[0], index[1] + offset[1])
            #print(f"{index} processing offset {offset} yielding {new_index}")

            if new_index[0] < 0 or new_index[1] < 0 or new_index[0] >= rows or new_index[1] >= cols:
                continue

            # To go offset, we must also traverse either vertically or horizontally
            if (dir == 'h'): O = space_height[new_index]
            else: O = space_width[new_index]

            if new_index == (2, 0) or new_index == (9,0):
                print(f"new_index={new_index} O={O} steps[new_index]={steps[new_index]} old_steps={old_steps}")

            if not new_index in visited: visit.add(new_index)

            if steps[new_index] == -1 or steps[new_index] > O + old_steps:
                # We haven't been here yet. So it just takes us the size of space steps to get here.
                steps[new_index] = O + old_steps
                visit.add(new_index)
            
    return steps

if __name__ == "__main__":

    lines = []
    for line in sys.stdin:
        line = line.strip()
        lines.append(line)

    rows = len(lines)
    cols = len(lines[0])
    galaxy = np.empty((rows, cols), dtype='str')
    galaxies = []
    for i, line in enumerate(lines):
        for j, c in enumerate(line):
            galaxy[i, j] = c
            if c == '#': galaxies.append((i, j))

    space_height = np.ones((rows, cols))
    space_width = np.ones((rows, cols))
    for i in range(rows):
        if np.sum(galaxy[i, :] == '#') == 0:
            space_height[i, :] = 2 * space_height[i, :]
    for i in range(cols):
        if np.sum(galaxy[:, i] == '#') == 0:
            space_width[:, i] = 2 * space_width[:, i]

    # g1 is at k1, k2
    # g2 is at m1, m2
    #  we need to step ... ()
    print(galaxies)
    print(space_height)
    print(space_width)
    total = 0
    results = {}
    for i, g in enumerate(galaxies):
        print(f"shortest path grid for {i} {g}:")
        d = shortestPath(g, space_height, space_width)
        print(d)
        for j, h in enumerate(galaxies):
            if (j < i and d[h] != results[j, i]):
                print("distance is not symmetric but we expected it to be.")
                print(f"(i, j) = {i}, {j} g, h = {g}, {h} d[h] = {d[h]} but results is {results[j, i]}")
                assert(d[h] == results[j, i])

            if j <= i: continue
            print(f"{i, j} => {d[h]}")
            results[i, j] = d[h]
            total += d[h]
    
    print(total)
