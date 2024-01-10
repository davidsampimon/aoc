import re


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
    # cmds, map_dict = data("input.txt")

    # searching = True
    # step = 0
    # length = len(cmds)
    # mp = "AAA"
    # while searching:
    #     mapping = map_dict[mp]
    #     action = cmds[step % length ]
    #     match action:
    #         case "L":
    #             mp = mapping[0]
    #         case "R":
    #             mp = mapping[1]
        
    #     if mp == "ZZZ":
    #         searching = False
        
    #     step += 1

    # print(f"Answer 1: {step}")

    # Puzzle 2
    cmds, map_dict = data("input.txt")
    starting_nodes = [key for key in list(map_dict.keys()) if key[2] == "A"]
    nodes = starting_nodes
    searching = True
    step = 0
    length = len(cmds)
    while searching:
        action = cmds[step % length]
        results = list()
        for node in nodes:
            mapping = map_dict[node]
            match action:
                case "L":
                    results.append(mapping[0])
                case "R":
                    results.append(mapping[1])


        if all(["Z" == key[2] for key in results]):
            searching = False
        
        nodes = results
        step += 1

    print(f"Answer 2: {step}")
    



