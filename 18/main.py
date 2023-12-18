import sys
import numpy as np

def printGrid(grid):
    print("")
    for row in range(grid.shape[0]):
        print(f"{row}\t{grid[row,:]}")
    print("")

def inbounds(index, anarray):
    return index[0] >= 0 and index[0] < anarray.shape[0] and index[1] >= 0 and index[1] < anarray.shape[1]

# Return a new tuple one step in that direction
def onestep(index, dir):
    y, x = index
    off = { 'R': (0, 1), 'L': (0, -1), 'U': (-1, 0), 'D': (1, 0) }[dir]
    return (y + off[0], x + off[1]) 

# Part 1
# Reads the dig plan into a numpy array
def importDigPlan(digplan):
    maxy = None
    maxx = None
    minx = None
    miny = None
    x = 0
    y = 0
    for dir, steps, color in digplan:
        if dir == 'R': x += steps
        if dir == 'L': x -= steps
        if dir == 'U': y -= steps
        if dir == 'D': y += steps

        if minx is None or (x < minx): minx = x
        if miny is None or (y < miny): miny = y
        if maxx is None or (x > maxx): maxx = x
        if maxy is None or (y > maxy): maxy = y
    
    grid = np.full((maxy-miny+1, maxx-minx+1), ' ', dtype='str')
    print(grid.shape)

    start = (0, 0)
    for dir, steps, color in digplan:
        y, x = start
        if dir == 'R': stop = (y, x + steps)
        if dir == 'L': stop = (y, x - steps)
        if dir == 'U': stop = (y - steps, x)
        if dir == 'D': stop = (y + steps, x)
        
        #print(f"start={start} stop={stop}")
        while start != stop:
            t = (start[0] - miny, start[1] - minx)
            grid[t] = '#'
            start = onestep(start, dir)
    return grid


# Part 2
# Reads the dig plan into a list of verticies
def importDigPlan2(digplan):
    maxy = None
    maxx = None
    minx = None
    miny = None
    x = 0
    y = 0
    points = []
    for dir, steps, color in digplan:
        points.append((y, x))
        if dir == 'R': x += steps
        if dir == 'L': x -= steps
        if dir == 'U': y -= steps
        if dir == 'D': y += steps

        if minx is None or (x < minx): minx = x
        if miny is None or (y < miny): miny = y
        if maxx is None or (x > maxx): maxx = x
        if maxy is None or (y > maxy): maxy = y
    return points

def padAndFlood(grid):
    biggrid = np.pad(grid, (1, 1), 'constant', constant_values = ' ')
    start_index = (0, 0)

    visited = set()
    visit = set()
    visit.add(start_index)
    biggrid[start_index] = '-'
    while len(visit) > 0:
        index = visit.pop()
        visited.add(index)
        for dir in ['U', 'D', 'L', 'R']:
            new_index = onestep(index, dir)
            if inbounds(new_index, biggrid) and new_index not in visited and biggrid[new_index] == ' ':
                biggrid[new_index] = '-'
                visit.add(new_index)
    return biggrid

# actually building the grid is impossible for part 2
#  without more RAM and a motherboard from the year 20240
# So I will try to use Shoelace formula instead.
# https://en.wikipedia.org/wiki/Shoelace_formula
def shoelaceIt(points):
    area = 0
    perimeter = 0

    for i, p in enumerate(points):
        if (i + 1) == len(points): j = 0
        else: j = i  + 1
        next = points[j]
        sub = p[1]*next[0] - next[1]*p[0]
        print(f"p = {p} next = {next} sub = {sub}")
        area += p[1]*next[0] - next[1]*p[0]
        perimeter += np.abs((p[1] - next[1]) + (p[0] - next[0]))

    print(f"after shoelace perimeter is {perimeter}")
    return (area / 2) + (perimeter / 2) + 1

if __name__ == "__main__":
    digplan = []
    for line in sys.stdin:
        line = line.strip()
        parts = line.split(' ')
        dir = parts[0]
        steps = int(parts[1])
        color = parts[2]
        # 012
        # (#0a7ad2)
        steps = int(parts[2][2:7], 16)
        dir = {0:'R',1:'D',2:'L',3:'U'}[int(parts[2][-2])]
        digplan.append((dir, steps, color))
    print(digplan)
    grid = importDigPlan2(digplan)
    print(grid)

    biggrid = shoelaceIt(grid)
    print(biggrid)
