import sys
import numpy as np
import re
from PIL import Image

# Coming in from the "top left" direction, 
# what is the output direction
#  North is (0, -1) and East is (1, 0) in this scheme.

heading_offset = {"E": ( 0,  1),"W": ( 0, -1),"N": (-1,  0),"S": ( 1,  0) }

def findStart(maze):
    for i, M in enumerate(maze):
        for j, em in enumerate(M):
            if em == 'S': return (i, j)
    raise RuntimeError("No start")

def tupleAdd(a, b): return (a[0]+b[0], a[1]+b[1])
def inbounds(index, maze):
    y, x = index
    return (y >= 0) and (y < len(maze)) and (x >= 0) and (x < len(maze[0]))
def charat(index, maze):
    assert(inbounds(index, maze))
    y, x = index
    return maze[y][x]

# For a given index and heading, will follow the maze
#  one step and return a (new index, new heading)
# our heading may change and then we take one step in heading direciton
def step(maze, index, heading):
    y = index[0]
    x = index[1]
    identity = { "S": "S", "N": "N", "E": "E", "W": "W"}
    newHeading = {
        "L": { "S": "E", "W": "N" },
        "J": { "E": "N", "S": "W" },
        "7": { "N": "W", "E": "S" },
        "F": { "N": "E", "W": "S" }
    }.get(maze[y][x], identity).get(heading, heading)
    # If the maze is one of LJ7F, use the special mapping; otherwise
    #  use the identity mapping (e.g. if you are going east you will continue to go east)
    # Then, immediately apply that map to the current heading to get the next heading.

    index = tupleAdd(index, heading_offset[newHeading])
    return (index, newHeading)
 

def countCrossings_prep5(index, maze, outside):
    Lookup5x5 = {
        "|": ["Ox.xO", "Ox.xO", "Ox.xO", "Ox.xO", "Ox.xO"],
        "-": ["OOOOO", "xxxxx", ".....", "xxxxx", "OOOOO"],
        "L": ["Ox.xO", "Ox.xx", "Ox...", "Oxxxx", "OOOOO"],
        "J": ["Ox.xO", "xx.xO", "...xO", "xxxxO", "OOOOO"],
        "7": ["OOOOO", "xxxxO", "...xO", "xx.xO", "Ox.xO"],
        "F": ["OOOOO", "Oxxxx", "Ox...", "Ox.xx", "Ox.xO"],
        ".": [".....", ".....", ".....", ".....", "....."]
    }

    result = np.empty(shape=(5*distance.shape[0], 5*distance.shape[1]), dtype='str')
    for i in range(distance.shape[0]):
        for j in range(distance.shape[1]):
            grid = Lookup5x5[maze[i][j]]
            new_i = 5*i
            new_j = 5*j

            outside = distance[i, j] == -999
            if outside: grid = ['OOOOO', 'OOOOO', 'OOOOO', 'OOOOO', 'OOOOO']
            # if we are not inside the maze, replace the .s with another
            # characeter. This will make a downstream algorithm easier
            for ii in range(5):
                for jj in range(5):
                    new_index = (new_i + ii, new_j + jj)
                    result[new_index] = grid[ii][jj]
    return result

def floodfill(anarray, start_index):
    # Flood O regions with the letter o.
    visited = set()
    visit = set()
    visit.add(start_index)
    anarray[start_index] = 'o'
    while len(visit) > 0:
        index = visit.pop()
        visited.add(index)
        for dir in heading_offset.keys():
            new_index = tupleAdd(index, heading_offset[dir])
            if inbounds(new_index, anarray) and new_index not in visited and anarray[new_index] == 'O':
                anarray[new_index] = 'o'
                visit.add(new_index)
    return anarray

if __name__ == "__main__":
    maze = []
    for line in sys.stdin:
        maze.append(line.strip())

    start = findStart(maze)
    
    # We are going to trace out all 4 possible routes from S
    #  simultaneously.  Where 2 of the routes meet will a) identify
    #  which of the routes is correct for the loop, but also will
    #  tell us how far apart we are.

    print(start)

    # Each of the routes are indexed by their original cardinal direction from S
    trial_starts = {
        direction: ( tupleAdd(start, heading_offset[direction])) for direction in ['E', 'W', 'N', 'S']
    }

    # Determine if any of these starts are valid.
    starts = {}
    print(trial_starts)
    for heading, index in trial_starts.items():
        isGood = True
        if (not inbounds(index, maze)):
            print(f"Eliminated {heading} becuase oob")
            isGood = False
        else:
            c = charat(index, maze)

            # Map of possible maze characters, and what headings are 'legal' for them
            islegal = {
                '|': "NS", 
                "-": "EW",
                "L": "SW",
                "J": "SE",
                "7": "NE",
                "F": "NW",
                ".": "",
            }
            if not heading in islegal[c]:
                print(f"Eliminated {heading} because {c} is not a valid space for heading {heading}")
                isGood = False

        if isGood: starts[heading] = index

    # Possible routes from start
    print(starts)

    distance = np.zeros((len(maze),len(maze[0]))) - 999
    distance[start] = 0
    for heading, index in starts.items():
        distance[index[0], index[1]] = 1

    # Before it was convienent to index these by their heading from the start
    # position, but very shortly those headings will not be guarenteed to be unique
    # So this is just to a list now, indexing the multiple tracers we have out in the maze.
    starts = list( (heading, index) for heading, index in starts.items() )

    step_num = 1
    loopFound = False
    while not loopFound:
        step_num += 1
        old_starts = starts.copy()
        starts = []
        
        for heading, index in old_starts:
            (next_index, next_heading) = step(maze, index, heading)
            c = maze[index[0]][index[1]]
            
            # have we been on this step before?
            if distance[next_index[0], next_index[1]] != -999:
                # we have, so we found the loop!
                loopFound = True
                break

            else:
                distance[next_index] = step_num
            starts.append( (next_heading, next_index))

    # We have to infer what S is now.  Eerg.
    S = { dir: distance[tupleAdd(start, heading_offset[dir])] for dir in heading_offset.keys() }
    key1 = None
    if S["E"] == 1: key1 = "E"
    elif S["W"] == 1: key1 = "W"
    key2 = None
    if S["N"] == 1: key2 = "N"
    elif S["S"] == 1: key2 = "S"

    s_must_be = {
        ("E", None): "_",
        (None, "N"): "|",
        ("E", "N"): "L",
        ("W", "N"): "J",
        ("E", "S"): "F",
        ("W", "S"): "7"
    }
    old_maze = maze[start[0]]
    print(f"Inferred S is {s_must_be[(key1, key2)]}")
    maze[start[0]] = old_maze[0:start[1]] + s_must_be[(key1, key2)] + old_maze[(start[1]+1):]

    # Blow up the maze by 5x. 
    X5 = countCrossings_prep5(None, maze, distance)
    # Pad the outside of the maze.  This guarentees connecting all outside regions
    X5 = np.pad(X5, (1, 1), 'constant', constant_values='O')
    # Start the floodfill at a known outside location
    X5 = floodfill(X5, (0,0))

    # What was not flood filled is either the maze or inside. 
    # Just count the numver of 5x5 insides.
    count = 0
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            allOs = True
            
            for ii in range(3):
                for jj in range(3):
                    index = (1 + 5*i + ii, 1 + 5*j + jj)
                    if X5[index] != 'O':
                        allOs = False
            if allOs: count += 1

    print(count)
 
    # Debugging Output
    img = Image.new('RGB', (len(X5[0]), len(X5)))
    pixels = img.load()
    for lineno, line in enumerate(X5):
        for colno, s in enumerate(line):
            if s == 'o': color = (255, 0, 0)
            elif s == 'O': color = (0, 255, 0)
            elif s == 'x': color = (0, 0, 0)
            elif s == '.': color = (255, 255, 255)
            pixels[colno, lineno] = color
    img.save("test.png")
    #print(inside_outside)
    #print(inside_points)
