


def shortest_path(pos, other):
    return (abs(pos[0] - other[0]) + abs(pos[1] - other[1]))


class Grid():
    def __init__(self, grid):
        self.map = grid
        self.size = (len(grid), len(grid[0]))
        self.expanded_map = list()
        self._expand()
        self.galaxies = list()
        self._find_galaxies()
        self.range_map = dict()
        self._fill_range_map()

    def _expand(self):
        for y in range(self.size[0]):
            row = self.row(y)
            self.expanded_map.append(row.copy())
            if self.is_empty(row):
                self.expanded_map.append(row.copy())

        empty_columns = list()
        for x in range(self.size[1]):
            column = self.column(x)
            if self.is_empty(column):
                empty_columns.append(x)

        for index, x in enumerate(empty_columns):
            target = index + x
            self._insert_empty_column(target, column)

    def _find_galaxies(self):
        height = len(self.expanded_map)
        width = len(self.expanded_map[0])

        for y in range(height):
            for x in range(width):
                if self.expanded_map[y][x] == "#":
                    self.galaxies.append((y, x))

    def _fill_range_map(self):
        for index_g, galaxy in enumerate(self.galaxies):
            for index_o, other in enumerate(self.galaxies):
                if galaxy == other:
                    continue
                key = tuple(sorted((index_g + 1, index_o + 1)))
                if key == (2, 0):
                    breakpoint()
                self.range_map[key] = shortest_path(galaxy, other)

    def _insert_empty_column(self, insert, column_data):
        for index, row in enumerate(self.expanded_map):
            row.insert(insert, ".")

    @staticmethod
    def is_empty(data_list):
        for symbol in data_list:
            if symbol == "#":
                return False
        return True

    def row(self, row_num):
        return self.map[row_num]

    def column(self, column_num):
        column_list = list()
        for y in range(self.size[0]):
            column_list.append(self.map[y][column_num])
        return column_list
    
    def draw(self, name="m"):
        match name:
            case "m":
                grid = self.map
            case "e":
                grid = self.expanded_map

        height = len(grid)
        width = len(grid[0])

        for y in range(height):
            print()
            for x in range(width):
                print(grid[y][x], end="")
        print()


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()
    
    for index, line in enumerate(lines):
        lines[index] = list(line)

    return Grid(lines)


if __name__ == "__main__":
    grid = data("input.txt")
    answer = 0
    breakpoint()
    for distance in grid.range_map.values():
        answer += distance

    print(f"Answer 1: {answer}")
