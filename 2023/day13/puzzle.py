class Grid():
    def __init__(self, grid):
        self.map = grid
        self.size = (len(grid), len(grid[0]))

    def row(self, num):
        try:
            return self.map[num]
        except IndexError:
            return None

    def column(self, num):
        column_data = list()
        try:
            for row in self.map:
                column_data.append(row[num])
            return column_data
        except IndexError:
            return None

    def is_mirror(self, num, d="h"):
        match d:
            case "h":
                rng = min(self.size[0]-(num + 1), num + 1)
                func = self.row
            case "v":
                rng = min(self.size[1]-(num + 1), num + 1)
                func = self.column

        if rng == 0:
            return False

        for i in range(rng):
            a = func(num - i)
            b = func(num + i + 1)
            if a != b:
                return False
        return True

    def diff_mirror(self, num, slack=1 ,d="h"):
        match d:
            case "h":
                rng = min(self.size[0]-(num + 1), num + 1)
                func = self.row
            case "v":
                rng = min(self.size[1]-(num + 1), num + 1)
                func = self.column

        if rng == 0:
            return False

        smudges = 0
        for i in range(rng):
            a = func(num - i)
            b = func(num + i + 1)
            mir = zip(a,b)
            smudges += len([c_a for c_a, c_b in mir if c_a != c_b])
            if smudges > 1:
                return False
        return smudges == 1


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    data_list = list()
    grid_list = list()
    for line in lines:
        if line == "":
            data_list.append(Grid(grid_list))
            grid_list = list()
        else:
            grid_list.append(line)
    data_list.append(Grid(grid_list))

    return data_list


if __name__ == "__main__":
    grids = data("input.txt")

    # Puzzle 1
    answer = 0
    for grid in grids:
        for y in range(grid.size[0]):
            if grid.is_mirror(y):
                answer += (y + 1) * 100

    for grid in grids:
        for x in range(grid.size[1]):
            if grid.is_mirror(x, d="v"):
                answer += x + 1
    print(f"Answer 1: {answer}")

    # Puzzle 2
    answer = 0
    for grid in grids:
        for y in range(grid.size[0]):
            if grid.diff_mirror(y):
                answer += (y + 1) * 100

    for grid in grids:
        for x in range(grid.size[1]):
            if grid.diff_mirror(x, d="v"):
                answer += x + 1

    print(f"Answer 2: {answer}")
