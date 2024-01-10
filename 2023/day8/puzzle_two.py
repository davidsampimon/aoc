import re
import math


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()
    
    commands = lines.pop(0)

    dat = dict()
    for line in lines:
        if "=" in line:
            dirty_line = line.split(" = ")
            key = dirty_line[0]
            left = dirty_line[1][1:4]
            right = dirty_line[1][6:9]
            dat[key] = (left, right)
    return commands, dat

if __name__ == "__main__":
    # Puzzle 2
    cmds, map_dict = data("input.txt")
    starting_nodes = [key for key in list(map_dict.keys()) if key[2] == "A"]
    nodes = starting_nodes
    length = len(cmds)

    step_map = {}
    for node in nodes:
        searching = True
        step_map[node] = list()
        step = 0
        mp = node
        while searching:
            index = step % length
            mapping = map_dict[mp]
            action = cmds[index]
            match action:
                case "L":
                    mp = mapping[0]
                case "R":
                    mp = mapping[1]
            
            step += 1
            if mp[2] == "Z":
                step_map[node].append(step)
                searching = False

    steps_lol = list(step_map.values())
    steps = [s[0] for s in steps_lol]
    print(f"Answer 2: {math.lcm(*steps)}")


