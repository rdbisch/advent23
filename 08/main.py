import sys

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

    state = 'AAA'
    step_count = 0
    while state != 'ZZZ':
        step_count += len(steps)
        for s in steps:
            if s == 'L': state = maps[state][0]
            elif s == 'R': state = maps[state][1]
            else: 
                raise RuntimeError(f"Invalid step direction {s} in steps {steps}")
    print(step_count)