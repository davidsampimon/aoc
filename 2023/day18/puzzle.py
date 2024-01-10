DIRECTIONS = {
    "R": (0, 1),
    "D": (1, 0),
    "L": (0, -1),
    "U": (-1, 0)
}


def within_bounds(pos, start_y, height, start_x, width):
    return start_y <= pos[0] <= height and start_x <= pos[1] <= width


def neighbours(pos):
    return [
        (pos[0], pos[1] + 1),
        (pos[0] + 1, pos[1]),
        (pos[0], pos[1] - 1),
        (pos[0] - 1, pos[1]),
    ]


def add(pos, other_pos):
    return (pos[0] + other_pos[0], pos[1] + other_pos[1])


def draw(grid, start_y, height, start_x, width):
    for y in range(start_y, height+1):
        print()
        for x in range(start_x, width+1):
            if (y, x) in grid:
                print("#", end="")
            else:
                print(".", end="")
    print()


def data(filepath):
    data_list = list()
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    for line in lines:
        dirty_data = line.split()
        data_list.append(
            {
                "direction": DIRECTIONS[dirty_data[0]],
                "amount": int(dirty_data[1]),
                "hex": dirty_data[2].replace("(", "").replace(")", "")
            }
        )

    return data_list


class Grid:
    def __init__(self, commands, pos=(0, 0)):
        grid = {}
        min_y, min_x, max_y, max_x = 0, 0, 0, 0
        for command in commands:
            for _ in range(command["amount"]):
                pos = add(pos, command["direction"])
                grid[pos] = command["hex"]
                min_y = min(min_y, pos[0])
                min_x = min(min_x, pos[1])
                max_y = max(max_y, pos[0])
                max_x = max(max_x, pos[1])
        self.min_y = min_y
        self.min_x = min_x
        self.max_y = max_y
        self.max_x = max_x
        self.map = grid

    def get(self, pos):
        return self.map.get(pos)


if __name__ == "__main__":
    commands = data("input.txt")
    grid = Grid(commands)

    # Puzzle 1
    start_y = grid.min_y - 1
    start_x = grid.min_x - 1
    height = grid.max_y + 1
    width = grid.max_x + 1

    anti_map = set()
    coords = {(start_y, start_x)}
    while coords:
        pos = coords.pop()
        if grid.get(pos):
            continue
        anti_map.add(pos)
        nbs = [
            nb for nb in neighbours(pos) if within_bounds(
                nb, start_y, height, start_x, width
            )
        ]
        for nb in nbs:
            if nb not in anti_map:
                coords.add(nb)

    area = (1 + height - start_y) * (1 + width - start_x) - len(anti_map)
    print(f"Answer 1: {area}")
