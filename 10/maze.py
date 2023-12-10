import sys
import numpy as np

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

    for heading, index in starts.items():
        distance[index[0], index[1]] = 1

    # Before it was convienent to index these by their heading from the start
    # position, but very shortly those headings will not be guarenteed to be unique
    # So this is just to a list now, indexing the multiple tracers we have out in the maze.
    starts = list( (heading, index) for heading, index in starts.items() )
    print(starts)

    step_num = 1
    loopFound = False
    while not loopFound:
        step_num += 1
        old_starts = starts.copy()
        starts = []
        print(f"old_starts={old_starts}")
        for heading, index in old_starts:
            (next_index, next_heading) = step(maze, index, heading)
            c = maze[index[0]][index[1]]
            print(f"main loop: {heading}, {index} [ {c} ]=> {next_heading} {next_index}")
            # have we been on this step before?
            if distance[next_index[0], next_index[1]] != -999:
                # we have, so we found the loop!
                loopFound = True
                break

            else:
                distance[next_index] = step_num
            starts.append( (next_heading, next_index))

    print(distance)
    print(step_num)
