import sys

UNREACH_VALUE = -1
ROCK_VALUE = -2

def find_neighbors(coord):
    return [
        (coord[0] - 1, coord[1], coord[2]),
        (coord[0] + 1, coord[1], coord[2]),
        (coord[0], coord[1] - 1, coord[2]),
        (coord[0], coord[1] + 1, coord[2]),
        (coord[0], coord[1], coord[2] - 1),
        (coord[0], coord[1], coord[2] + 1)
    ]

class Cube:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.neighbors = find_neighbors((x, y, z))
        self.visible_sides = 6

    @property
    def position(self):
        return (self.x, self.y, self.z)

    def set_visible_sides(self, sides):
        self.visible_sides = sides

    def __repr__(self):
        return f"Cube(x={self.x}, y={self.y}, z={self.z})"
    
    def __eq__(self, other):
        return self.position == other

class Grid:
    def __init__(self, cube_data):
        self.cube_list = cube_data
        self.x = self._init_axis(0)
        self.y = self._init_axis(1)
        self.z = self._init_axis(2)
        self._init_visible_sides()
        self.total_surface_area = self._init_surface_area()
        self.grid = [[[]]]
        self._init_grid()

    def _init_visible_sides(self):
        for cube in self.cube_list:
            hit_count = 0
            for neighbor in cube.neighbors:
                if neighbor in self.cube_list:
                    hit_count += 1
            visible_sides = 6 - hit_count
            cube.set_visible_sides(visible_sides)

    def _init_surface_area(self):
        total = 0
        for cube in self.cube_list:
            total += cube.visible_sides
        return total
    
    def _init_axis(self, index):
        max_axis = 0
        for cube in self.cube_list:
            max_axis = max(cube.position[index], max_axis)
        return max_axis

    def _init_grid(self):
        self.grid = [
            [
                [-1 for _ in range(self.z + 1)] for _ in range(self.y + 1)
            ] for _ in range(self.x + 1)
        ]
        for cube in self.cube_list:
            self.add_to_grid(cube.position, ROCK_VALUE)

    def add_to_grid(self, coord, value):
        self.grid[coord[0] - 1][coord[1] - 1][coord[2] - 1] = value


    def check_grid(self, coord):
        return self.grid[coord[0] - 1][coord[1] - 1][coord[2] - 1]
    

    def within_bounds(self, coord):
        return 0 <= coord[0] <= self.x and \
               0 <= coord[1] <= self.y and \
               0 <= coord[2] <= self.z
    
    def bfs(self, pos, count=0):
        self.add_to_grid(pos, count)
        neighbors = find_neighbors(pos)
        for neighbor in neighbors:
            steps = self.check_grid(neighbor)
            if self.within_bounds(neighbor) and neighbor != ROCK_VALUE:
                if steps == UNREACH_VALUE or steps > count + 1:
                    self.bfs(neighbor, count+1)

    def find_pockets(self, value):
        pocket_list = []
        for x_index, col_yz in enumerate(self.grid):
            for y_index, col in enumerate(col_yz):
                for z_index, step in enumerate(col):
                    if step == value:
                        pocket_list.append(
                            (
                                x_index + 1,
                                y_index + 1,
                                z_index + 1
                                )
                            )
        return pocket_list

def parse_input(data):
    with open(data, "r") as f:
        data_list = f.read().splitlines()
    
    cube_list = []
    for coord_string in data_list:
        coord = coord_string.split(",")
        cube_list.append(
            Cube(
                int(coord[0]),
                int(coord[1]),
                int(coord[2])
            )
        )
    return cube_list

def main():
    cube_list = parse_input("input.txt")
    grid = Grid(cube_list)
    # answer puzzle 1
    answer_one = grid.total_surface_area
    print(answer_one)
    # answer puzzle 2
    sys.setrecursionlimit(10**6)
    grid.bfs((0,0,0))
    pockets = grid.find_pockets(-1)
    surface_counter = 0
    for pos in pockets:
        neighbors = find_neighbors(pos)
        for neighbor in neighbors:
            if grid.check_grid(neighbor) == ROCK_VALUE:
                surface_counter += 1

    answer_two = answer_one - surface_counter
    print(answer_two)

if __name__ == "__main__":
    main()
