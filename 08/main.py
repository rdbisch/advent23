import sys
import math

# OK for step2 this is intractable.   New idea.
# Assume that STEPS has to be taken whole.  This means that
#   s1 => (LR)+ => sk

# Is really the only computation we have to do for each state.
#  We shoul be able to determine, from the set of all possible states,
#  which of these will terminate in a Z.  
_applySteps_memo = {}
def applySteps(state, steps, maps):
    global _applySteps_memo
    if state in _applySteps_memo:
        return _applySteps_memo[state]

    original_state = state
    step_count = 0
    step_count += len(steps)
    for s in steps:
        if s == 'L': state = maps[state][0]
        elif s == 'R': state = maps[state][1]
        else: 
            raise RuntimeError(f"Invalid step direction {s} in steps {steps}")

    _applySteps_memo[original_state] = state
    return state

# Repeatedly apply steps until state ends in Z
def repeatedApplication(state, steps, maps):
    trial = 0 
    while (state[-1] != 'Z'):
        state = applySteps(state, steps, maps)
        trial = trial + 1
    return trial*len(steps)


# from 
# https://stackoverflow.com/questions/37237954/calculate-the-lcm-of-a-list-of-given-numbers-in-python
# 12/9/23
def lcm(a):
    lcm = 1
    for i in a:
        lcm = lcm*i//math.gcd(lcm, i)
    return(lcm)

if __name__ == "__main__":
    state = 0
    steps = ""
    maps = {}

    for line in sys.stdin:
        line = line.strip()
        if state == 0:
            steps = line
            state = 1
        elif state == 1:
            if line != "":
                raise RuntimeError("Expected blank line. Got {line}")
            else: state = 2
        elif state == 2:
            if line == "": continue
            node = line.split('=')[0].strip()
            left = line.split('=')[1].split(',')[0][2:]
            right = line.split('=')[1].split(',')[1][1:-1]
            print(f"node={node} => (left={left}, right={right}) from line {line}")
            maps[node] = (left, right)

    memo = {}
    step_count = 0
    states = [ k for k in maps.keys() if k[-1] == 'A' ]
    numbers = [ repeatedApplication(s, steps, maps) for s in states ]
    print(lcm(numbers))
 