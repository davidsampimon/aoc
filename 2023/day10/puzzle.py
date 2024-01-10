import sys
sys.setrecursionlimit(100000)

MOVES = {
    "|": [(-1, 0), (1, 0)],
    "-": [(0, -1), (0, 1)],
    "L": [(-1, 0), (0, 1)],
    "J": [(-1, 0), (0, -1)],
    "7": [(0, -1), (1, 0)],
    "F": [(1, 0), (0, 1)],
}

CONNECTOR = {
    (0, 1): "F",
    (0, 2): "-",
    (0, 3): "L",
    (1, 2): "7",
    (1, 3): "|",
    (2, 3): "J",
}


def neighbour(coord):
    y = coord[0]
    x = coord[1]
    return [
        (y, x+1),
        (y+1, x),
        (y, x-1),
        (y-1, x)
    ]


def add(coord, diff):
    return (coord[0] + diff[0], coord[1] + diff[1])


class Grid():
    def __init__(self, grid, size, start):
        self.map = grid
        self.size = size
        self.start = start
        self.step_map = dict()
        self.traverse(start)
        self.clean_map = dict()
        self.cleanup()

    def traverse(self, pos, step=0):
        count = self.step_map.get(pos, step+1)
        if count < step:
            return

        self.step_map[pos] = step

        connect = self.connects(pos)
        valid_nb = list()
        for nb in connect:
            if pos in self.connects(nb):
                valid_nb.append(nb)

        for nb in valid_nb:
            self.traverse(nb, step+1)
        return

    def connects(self, pos):
        symbol = self.map.get(pos)
        if symbol == "S":
            return neighbour(pos)

        moves = MOVES[symbol]
        return [add(pos, diff) for diff in moves]

    def cleanup(self):
        for pos in self.step_map:
            self.clean_map[pos] = self.map[pos]

        connector = list()
        for index, nb in enumerate(neighbour(self.start)):
            if self.step_map.get(nb) == 1:
                connector.append(index)
        connect = (connector[0], connector[1])
        self.clean_map[self.start] = CONNECTOR[connect]

    def is_inside(self, pos):
        collission = list()
        for y in range(pos[0], self.size[0]):
            symbol = self.clean_map.get((y, pos[1]))
            if symbol in ["S", "-", "F", "7", "L", "J"]:
                collission.append(symbol)

        hits = 0
        for index, symbol in enumerate(collission):
            if symbol == "-":
                hits += 1
            if symbol == "F" and collission[index + 1] == "J":
                hits += 1
            if symbol == "7" and collission[index + 1] == "L":
                hits += 1

        return hits % 2 == 1

    def encapsulated_count(self):
        height = self.size[0]
        width = self.size[1]

        count = 0
        for y in range(height):
            for x in range(width):
                pos = (y, x)
                if pos not in self.clean_map:
                    if self.is_inside(pos):
                        count += 1

        return count


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    grid = dict()
    for y, line in enumerate(lines):
        for x, symbol in enumerate(line):
            if symbol == "S":
                grid[(y, x)] = symbol
                start_pos = (y, x)
            elif symbol != ".":
                grid[(y, x)] = symbol

    size = (len(lines), len(line))
    return Grid(grid, size, start_pos)


if __name__ == "__main__":
    grid = data("input.txt")
    answer = max(grid.step_map.values())
    print(f"Answer 1: {answer}")
    print(f"Answer 2: {grid.encapsulated_count()}")
