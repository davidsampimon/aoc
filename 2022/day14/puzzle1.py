from copy import deepcopy


class Sand:
    def __init__(self, coord):
        self.symbol = "o"
        self.coord = coord

    @property
    def options(self):
        y = self.coord[0]
        x = self.coord[1]
        return (y + 1, x), (y + 1, x - 1), (y + 1, x + 1)


class Grid:
    def __init__(self, rock_list, floor=False):
        self.rocks = self._fill_rocks(rock_list)
        self.center = 500
        self.start_height = 0
        self.rocks_y, self.rocks_x = self._size()
        self.y_offset = self.rocks_y[0]
        self.x_offset = self.rocks_x[0]
        self.grid = [[],[]]
        self._grid_init(floor)
        
    @property
    def y(self):
        return len(self.grid)
    
    @property
    def x(self):
        return len(self.grid[0])

    @property
    def drip_point(self):
        return (0, self.grid[0].index("+") + self.x_offset)

    def _grid_init(self, floor=False):
        if floor:
            self.rocks_y = (self.rocks_y[0], self.rocks_y[1] + 2)

        self.grid = [
            ["." for x in range(0, 1 + self.rocks_x[1] - self.x_offset)] for y in range(0, 3 + self.rocks_y[1] - self.y_offset)
        ]

        for y in range(self.rocks_y[0], self.rocks_y[1] + 3):
            for x in range(self.rocks_x[0], self.rocks_x[1] + 1):
                if (y, x) in self.rocks:
                    self.add_item((y, x), "#")
                if floor and y is self.rocks_y[1]:
                    self.add_item((y, x), "#")
        self.add_item((0, self.center), "+")
    
    def is_free(self, coord):
        # if not self.on_grid(coord):
        #     self.increase_grid(coord)
        #     coord = (coord[0], coord[1] + 1)
        try:
            return \
                self.grid[coord[0] - self.y_offset][coord[1] - self.x_offset] == "."
        except Exception as e:
            raise Exception(f"Out of bounds {coord}: {e}")
    
    def on_grid(self, coord):
        y = coord[0] - self.y_offset
        x = coord[1] - self.x_offset
        return 0 <= x < self.x and 0 <= y <= self.y
           
    
    def increase_grid(self, coord):
        y = coord[0] - self.y_offset
        x = coord[1] - self.x_offset
        x_min = 0
        x_max = self.x

        if x >= x_max:
            for index, y in enumerate(self.grid):
                if index == 179:
                    symbol = "#"
                else:
                    symbol = "."
                y.append(symbol)
            return 0
        
        if x < x_min:
            for index, y in enumerate(self.grid):
                if index == 179:
                    symbol = "#"
                else:
                    symbol = "."
                y.insert(0, symbol)
            self.x_offset -= 1
            self.center += 1
            return 1
        return 0


    def _fill_rocks(self, rock_list):
        rocks = []
        for row in rock_list:
            lines = len(row)-1
            for index in range(lines):
                y_from = min(row[index][0], row[index+1][0])
                y_to = max(row[index][0], row[index+1][0])
                x_from = min(row[index][1], row[index+1][1])
                x_to = max(row[index][1], row[index+1][1])
                for y in range(y_from, y_to + 1):
                    for x in range(x_from, x_to + 1):
                        rocks.append((y, x))
        return rocks

    def _size(self):
        max_y = self.start_height
        min_y = self.start_height
        max_x = self.center
        min_x = self.center
        for rock in self.rocks:
            max_y = max(max_y, rock[0])
            min_y = min(min_y, rock[0])

            max_x = max(max_x, rock[1])
            min_x = min(min_x, rock[1])
        return (min_y, max_y), (min_x, max_x)

    def draw(self):
        draw_width = min(self.x, 80)
        half_width = draw_width // 2

        if "+" in self.grid[0]:
            center = self.grid[0].index("+")
        else:
            center = self.grid[0].index("o")

        start_x = center - half_width
        end_x = center + half_width

        for line in self.grid:
            print()
            for index in range(start_x, end_x):
                print(line[index], end="")
        print()

    def add_item(self, coord, symbol):
        self.grid[coord[0]-self.y_offset][coord[1]-self.x_offset] = symbol

    def check_down(self, coord):
        positions = [
            (coord[0] + 1, coord[1]),
            (coord[0] + 1, coord[1] - 1),
            (coord[0] + 1, coord[1] + 1)
        ]

        for pos in positions:
            if self.is_free(pos):
                return pos
        return False


    def reset(self, floor=False):
        self._grid_init(floor)


def parse_input(data):
    result = []
    elements = []
    with open(data, "r") as f:
        total_lines = f.read().splitlines()

    for line in total_lines:
        cleaned_lines = line.split(" -> ")
        for element in cleaned_lines:
            elements.append(get_coord(element))
        result.append(deepcopy(elements))
        elements = []
    return result

def get_coord(point_string):
    x = int(point_string.split(",")[0])
    y = int(point_string.split(",")[1])
    return (y, x)

if __name__ == "__main__":
    data = parse_input("input.txt")
    grid = Grid(data)

    # puzzle 1
    sand_pour = True
    abyss = grid.rocks_y[1]
    answer = 0
    while sand_pour:
        falling = True
        sand = Sand(grid.drip_point)
        while falling:
            if grid.check_down(sand.coord):
                sand.coord = grid.check_down(sand.coord)
            else:
                falling = False
                grid.add_item(sand.coord, sand.symbol)
                answer += 1
            if sand.coord[0] > abyss:
                falling = False
                sand_pour = False
                break
    grid.draw()
    print(answer)
    breakpoint()

    # puzzle 2
    grid = Grid(data, floor=True)
    # grid.reset(floor=True)
    answer = 0
    sand_pour = True
    sand_counter = 0
    while sand_pour:
        falling = True
        sand = Sand(grid.drip_point)
        sand_counter += 1
        while falling:
            for pos in sand.options:
                if not grid.on_grid(pos):
                    offset = grid.increase_grid(pos)
                    sand.coord = (sand.coord[0], sand.coord[1] + offset)
            if grid.check_down(sand.coord):
                sand.coord = grid.check_down(sand.coord)
            else:
                falling = False
                grid.add_item(sand.coord, sand.symbol)
                answer += 1
            if sand.coord[0] == 0:
                falling = False
                sand_pour = False
                break

    print(sand_counter)
    breakpoint()
