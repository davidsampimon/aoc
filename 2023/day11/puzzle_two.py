
def shortest_path(pos, other):
    return (abs(pos[0] - other[0]) + abs(pos[1] - other[1]))

class Grid():
    def __init__(self, grid):
        self.map = grid
        self.size = (len(grid), len(grid[0]))
        self.expand_factor = 1000000 - 1
        self.galaxies = dict()
        self.range_map = dict()
        self._find_galaxies()
        self._expand()
        self._fill_range_map()

    def _find_galaxies(self):
        height = len(self.map)
        width = len(self.map[0])

        for y in range(height):
            for x in range(width):
                if self.map[y][x] == "#":
                    self.galaxies[(y, x)] = (y, x)
    
    def _fill_range_map(self):
        for key_i, pos_i in self.galaxies.items():
            for key_j, pos_j in self.galaxies.items():
                if key_i == key_j:
                    continue
                key = tuple(sorted((key_i, key_j)))
                self.range_map[key] = shortest_path(pos_i, pos_j)

    def row(self, row_num):
        return self.map[row_num]

    def column(self, column_num):
        column_list = list()
        for y in range(self.size[0]):
            column_list.append(self.map[y][column_num])
        return column_list

    @staticmethod
    def is_empty(data_list):
        for symbol in data_list:
            if symbol == "#":
                return False
        return True
    
    def _expand(self):
        height = self.size[0]
        width = self.size[1]

        for y in range(height):
            if self.is_empty(self.row(y)):
                em = [g_key for g_key in self.galaxies.keys() if g_key[0] > y]
                for galaxy in em:
                    dis_y, dis_x = self.galaxies[galaxy]
                    dis_y += self.expand_factor
                    self.galaxies[galaxy] = (dis_y, dis_x)

        for x in range(width):
            if self.is_empty(self.column(x)):
                em = [g_key for g_key in self.galaxies.keys() if g_key[1] > x]
                for galaxy in em:
                    dis_y, dis_x = self.galaxies[galaxy]
                    dis_x += self.expand_factor
                    self.galaxies[galaxy] = (dis_y, dis_x)


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()
    
    for index, line in enumerate(lines):
        lines[index] = list(line)

    return Grid(lines)

if __name__ == "__main__":
    grid = data("input.txt")
    answer = 0
    for distance in grid.range_map.values():
        answer += distance

    print(f"Answer 2: {answer}")
    breakpoint()
