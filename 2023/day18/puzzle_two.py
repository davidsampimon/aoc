DIRECTIONS = {
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
    "U": (-1, 0)
}

NUMS = {
    "0": "R",
    "1": "D",
    "2": "L",
    "3": "U",
}


def multiply(pos, multiple):
    return (pos[0] * multiple, pos[1] * multiple)


def add(pos, other_pos):
    return (pos[0] + other_pos[0], pos[1] + other_pos[1])


def cmds_to_points(commands):
    coords = [(0, 0)]
    for cmd in commands:
        delta = multiply(cmd[0], cmd[1])
        pos = add(coords[-1], delta)
        coords.append(pos)
    return coords


def hex_to_dig(hex):
    direction = DIRECTIONS[NUMS[hex[-1]]]
    num = int(hex[:-1].replace("#", ""), 16)

    return (direction, num)


def area(points):
    results = 0

    for index in range(len(points)):
        p = points[index - 1]
        q = points[index]
        results += (p[0] - q[0]) * (p[1] + p[1])

    return abs(results) / 2


def data(filepath):
    data_list = list()
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    for line in lines:
        dirty_data = line.split()
        data_list.append(
            hex_to_dig(
                dirty_data[2].replace("(", "").replace(")", "")
            )
        )

    return data_list


if __name__ == "__main__":
    commands = data("input.txt")
    points = cmds_to_points(commands)
    inner_area = area(points)
    circum = sum([length for point, length in commands])
    answer = inner_area + circum/2 + 1
    print(f"Answer 2: {int(answer)}")
