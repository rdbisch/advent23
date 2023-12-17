import sys
import numpy as np
import heapq

def inbounds(point, grid):
    return point[0] >= 0 and point[1] >= 0 and point[0] < grid.shape[0] and point[1] < grid.shape[1]

def extend(point, direction, distance = 1):
    point_x = { "E": -1, "W": 1 }
    point_y = { "N": -1, "S": 1 }
    return (point[0] + distance * point_y.get(direction, 0),
            point[1] + distance * point_x.get(direction, 0))

def inferDirection(x, y):
    if (x[0] == y[0]): return 'E' if y[1] < x[1] else 'W'
    else: return 'N' if y[0] < x[0] else 'S'
    
def makeMoves2(grid, point):
    # Grid is now a 2xNxN and the moves can only be between planes not within.
    moves = []
    q = 1 if point[0] == 0 else 0

    for d in ['N', 'S', 'E', 'W']:
        if point[0] == 0 and d in ('E', 'W'): continue
        elif point[0] == 1 and d in ('N', 'S'): continue

        cost = 0
        for spaces in range(1, 11):
            pt = extend((point[1], point[2]), d, spaces)
            if inbounds(pt, np.zeros(grid.shape[1:])): # hackery
                p = (q, pt[0], pt[1])
                cost += grid[p]
                if spaces >= 4: moves.append({"from": point, "to": p, "cost": cost})
    return moves

def makeMoves(grid, point, lastMove = None):  #todo lastmove
    # We can move orthogonally up to three different grids in each cardinal direction
    moves = []
    for d in ['N', 'S', 'W', 'E']:
        # force only perpendicular moves
        if lastMove != None:
            if lastMove in ['N', 'S'] and d in ['N', 'S']: continue
            if lastMove in ['E', 'W'] and d in ['E', 'W']: continue

        cost = 0
        for spaces in range(1, 4):
            p = extend(point, d, spaces)
            if inbounds(p, grid):
                cost += grid[p]
                moves.append({"from": point, "to": p, "cost": cost})
    return moves

# Straight forward Djikstra doesnt work because the edges/nodes depend on the path
# we took to get here.
#  But I think the path really only matters in terms of the node - did we get here
#   from the EW line or the NS line?  
# So maybe straight forward Djikstra can work if we artificially create a 3rd dimension
#  of nodes.  e.g. (1,1,Up)    both represent grid square 1,1 physically
#                  (1,1,Left) 
#
#  The edges of (1,1,Up) are then all (1,x,Left)
#   and the edges of (1,1,Left) are similarly (x, 1, Up)
def djikstra(grid, source, target):
    cost = -np.ones(grid.shape)
    cost[source] = 0

    predecessor_y = np.zeros(grid.shape, dtype='int')
    predecessor_x = np.zeros(grid.shape, dtype='int')
    lastMove = np.full(grid.shape, fill_value='?')
    
    # triple: (cost, dim 0 index, dim 1 index)
    unvisited = np.ones(grid.shape)

    while np.sum(unvisited) > 0:
        # Get the lowest cost univisted node
        #  (cost < 0 ==> infinity)
        indices = np.where( np.logical_and(unvisited > 0, cost >= 0 ) )
        # give me the index of the lowest cost
        #   square on the grid that we have not yet visited.
        next_t = np.where( cost[indices] == min(cost[indices]) )
        next = indices[0][ next_t[0][0] ], indices[1][ next_t[0][0] ]
        current_cost = cost[next]

        print(f"Working on {next} with current cost {current_cost}")

        connections = makeMoves(grid, next, lastMove[next])

        for adict in connections:
            _from, _to, _cost = adict["from"], adict["to"], adict["cost"]
            print(f"...{_from}->{_to}@{_cost}? cost[_to]={cost[_to]} ...")
            if unvisited[_to] == 1:
                if (cost[_to] < 0) or current_cost + _cost < cost[_to]:
                    cost[_to] = current_cost + _cost
                    predecessor_x[_to] = next[1]
                    predecessor_y[_to] = next[0]
                    lastMove[_to] = inferDirection(next, _to)
        
        unvisited[next] = 0 
        if next == target:
            y = target
            steps = np.zeros(grid.shape)
            stepno = -1
            while y != source:
                print(f"node {y} cost {cost[y]} lastMove {lastMove[y]}")
                steps[y] = stepno
                stepno = stepno - 1
                y = predecessor_y[y], predecessor_x[y]
            steps[steps<0] = steps[steps<0] - np.min(steps) + 2
            steps[source] = 1
            print(steps) 
            print(f"cost:\n{cost}\npred_y\n{predecessor_y}\n\n{predecessor_x}\n\n{lastMove}")
            return cost[next]
        
    print(f"cost:\n{cost}\npred_y\n{predecessor_y}\n\n{predecessor_x}")
    print("Target not reachable")

def djikstra2(grid, source, target):
    new_grid = np.zeros((2, grid.shape[0], grid.shape[1]))
    new_grid[0] = grid
    new_grid[1] = grid

    cost = -np.ones(new_grid.shape)
    cost[0, source[0], source[1]] = 0
    cost[1, source[0], source[1]] = 0

    predecessor_y = np.zeros(new_grid.shape, dtype='int')
    predecessor_x = np.zeros(new_grid.shape, dtype='int')
    
    # triple: (cost, dim 0 index, dim 1 index)
    unvisited = np.ones(new_grid.shape)

    while np.sum(unvisited) > 0:
        # Get the lowest cost univisted node
        #  (cost < 0 ==> infinity)
        indices = np.where( np.logical_and(unvisited > 0, cost >= 0 ) )

        if len(indices[0]) == 0:
            # There are unvisited nodes but they are unreachable
            break
 
        # give me the index of the lowest cost
        #   square on the grid that we have not yet visited.
        next_t = np.where( cost[indices] == min(cost[indices]) )
        next = indices[0][ next_t[0][0] ], indices[1][ next_t[0][0] ], indices[2][ next_t[0][0] ]
        assert(unvisited[next] > 0)
        current_cost = cost[next]

        #print(f"Working on {next} with current cost {current_cost}")

        connections = makeMoves2(new_grid, next)

        for adict in connections:
            _from, _to, _cost = adict["from"], adict["to"], adict["cost"]
            debug_str1 = f"...{_from}->{_to}@{_cost}? cost[_to]={cost[_to]} ..."
            if unvisited[_to] == 1:
                if (cost[_to] < 0) or current_cost + _cost < cost[_to]:
                    cost[_to] = current_cost + _cost
                    predecessor_x[_to] = next[1]
                    predecessor_y[_to] = next[0]
                #print(f"{debug_str1} ... YES")
            else:
                pass
                #print(f"{debug_str1} ... NO")
        unvisited[next] = 0 
    
    return min(cost[0, target[0], target[1]], cost[1, target[0], target[1]])
    print(cost[0])
    print('\n\n')
    print(cost[1])
    #print(f"cost:\n{cost}\npred_y\n{predecessor_y}\n\n{predecessor_x}")
    print("Target not reachable")

"""         if next[1:] == target:
            y = target
            steps = np.zeros(grid.shape)
            stepno = -1
            while y[1:] != source:
                print(f"node {y} cost {cost[y]}")
                steps[y] = stepno
                stepno = stepno - 1
                y = predecessor_y[y], predecessor_x[y]
            steps[steps<0] = steps[steps<0] - np.min(steps) + 2
            steps[source] = 1
            print(steps) 
            print(f"cost:\n{cost}\npred_y\n{predecessor_y}\n\n{predecessor_x}\n\n")
            return cost[next] """




if __name__ == "__main__":
    lines = []
    for line in sys.stdin:
        line=line.strip()
        lines.append(line)
    
    grid = np.zeros((len(lines), len(lines[0])))
    for i, line in enumerate(lines):
        grid[i, :] = [ int(x) for x in list(line) ]   # "2345" -> ["2", "3", "4", "5"] -> [2,3,4,5]
    print(grid)
    print(djikstra2(grid, (0,0), (grid.shape[0] - 1, grid.shape[1] - 1)))





    
