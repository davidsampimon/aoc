import re

NONEXIST = -1

def get_neighbors(pos):
    x = pos[0]
    y = pos[1]
    return [
        (x + 1, y),
        (x, y + 1),
        (x - 1, y),
        (x, y - 1)
    ]

def get_facing(from_pos, to_pos):
    if from_pos[0] < to_pos[0]:
        return 0
    if from_pos[1] < to_pos[1]:
        return 1
    if from_pos[0] > to_pos[0]:
        return 2
    if from_pos[1] > to_pos[1]:
        return 3

class Player:
    def __init__(self, pos):
        self.pos = pos
        # 0 = west, 1 = south, 2 = east, 3 = north
        self.facing = 0
        self.history = {pos: self.facing}

    def set_pos(self, pos):
        self.history[pos] = self.facing
        self.pos = pos
    
    def set_direction(self, facing):
        self.history[self.pos] = self.facing
        self.facing = (facing % 4)
    
    def rotate(self, action):
        match action:
            case "L":
                self.set_direction(self.facing - 1)
            case "R":
                self.set_direction(self.facing + 1)
            case _:
                raise Exception(f"Unknown action: {action}")

    @property
    def next(self):
        pos = self.pos
        match self.facing:
            case 0:
                return (pos[0] + 1, pos[1])
            case 1:
                return (pos[0], pos[1] + 1)
            case 2:
                return (pos[0] - 1, pos[1])
            case 3:
                return (pos[0], pos[1] - 1)

    def move(self):
        pos = self.pos
        match self.facing:
            case 0:
                return pos, (pos[0] + 1, pos[1])
            case 1:
                return pos, (pos[0], pos[1] + 1)
            case 2:
                return pos, (pos[0] - 1, pos[1])
            case 3:
                return pos, (pos[0], pos[1] - 1)

class Cube:
    def __init__(self, grid, grid_map):
        self.grid = grid
        self.max_y = len(grid)
        self.max_x = len(grid[0])
        self.side = max(self.max_y, self.max_x) // 4
        self.grid_map = grid_map
        self.corners = self._init_corners()
        self.inside_corners = self._init_ic()
        self.stitch_map = {}
        self._init_stitch_map()
    
    def draw(self):
        for y in range(self.max_y):
            print()
            for x in range(self.max_x):
                value = self.grid[y][x]
                if value == NONEXIST:
                    print(" ", end="")
                    continue
                print(self.grid[y][x], end="")
        print()
    
    def check_grid(self, pos):
        return self.grid[pos[1] - 1][pos[0] - 1]

    def _init_corners(self):
        corners = []
        sy = self.max_y // self.side
        sx = self.max_x // self.side

        for y in range(sy):
            for x in range(sx):
                start_y = y * self.side
                start_x = x * self.side
                left_top = (start_x + 1, start_y + 1)
                right_top = (start_x + self.side, start_y + 1)
                left_bottom = (start_x + 1, start_y + self.side)
                right_bottom = (start_x + self.side, start_y + self.side)
                corners += [left_top, right_top, right_bottom, left_bottom]
        return corners

    def _init_ic(self):
        ic = []
        for corner in self.corners:
            if self.check_grid(corner) != NONEXIST:
                continue
            neighbors = get_neighbors(corner)
            on_map_count = 0
            for neighbor in neighbors:
                if neighbor in self.grid_map:
                    on_map_count += 1
                if on_map_count == 2:
                    ic.append(corner)
                    break
        return ic
    
    def _init_facing(self, set_pos, other_pos, corner):
        if set_pos[0] == corner[0]:
            if set_pos[0] < other_pos[0]:
                return 2
            else:
                return 0
        if set_pos[1] == corner[1]:
            if set_pos[1] > other_pos[1]:
                return 1
            else:
                return 3

    def _get_runners(self, corner):
        neighbors = get_neighbors(corner)
        runners = [Player(pos) for pos in neighbors if pos in self.grid_map]
        r_one = runners[0]
        r_two = runners[1]
        r_one.facing = self._init_facing(r_one.pos, r_two.pos, corner)
        r_two.facing = self._init_facing(r_two.pos, r_one.pos, corner)
        return r_one, r_two
    
    def valid_corner(self, r_one, r_two):
        return r_one.next in self.grid_map or r_two.next in self.grid_map

    def corner_logic(self, runners):
        if (
            runners[0].next in self.grid_map 
            and runners[1].next in self.grid_map
            ):
            runners[0].pos = runners[0].next
            runners[1].pos = runners[1].next
            return runners
    
        for runner in runners:
            if runner.next in self.grid_map:
                runner.pos = runner.next
                continue
            old_void_facing = runner.void_facing

            neighbors = get_neighbors(runner.pos)
            for neighbor in neighbors:
                if (neighbor, old_void_facing) in self.stitch_map:
                    continue
                
                if neighbor in self.grid_map:
                    old = runner.facing
                    runner.facing = get_facing(runner.pos, neighbor)
                    new = runner.facing
                    delta = old - new
                    runner.void_facing = (
                        runner.void_facing - delta) % 4
        return runners[0], runners[1]

    def add_to_stitch_map(self, r_one, r_two):
        self.stitch_map[(r_one.pos, r_one.void_facing)] = (
            (r_two.pos, (r_two.void_facing + 2) % 4)
        )
        self.stitch_map[(r_two.pos, r_two.void_facing)] = (
            (r_one.pos, (r_one.void_facing + 2) % 4)
        )
        
    def _init_stitch_map(self):
        for corner in self.inside_corners:
            r_one, r_two = self._get_runners(corner)
            r_one.void_facing = get_facing(r_one.pos, corner)
            r_two.void_facing = get_facing(r_two.pos, corner)
            valid_run = True
            while valid_run:
                for _ in range(self.side - 1):
                    self.add_to_stitch_map(r_one, r_two)
                    r_one.pos = r_one.next
                    r_two.pos = r_two.next
                if self.valid_corner(r_one, r_two):
                    self.add_to_stitch_map(r_one, r_two)
                    r_one, r_two = self.corner_logic([r_one, r_two])
                else:
                    self.add_to_stitch_map(r_one, r_two)
                    valid_run = False

def draw_grid(grid, player):
    height = len(grid)
    width = len(grid[0])
    p_pos = player.pos

    for y in range(height):
        print()
        for x in range(width):
            if (x+1, y+1) == p_pos:
                print("P", end="")
                continue
            
            if (x+1, y+1) in player.history:
                facing = player.history[(x+1, y+1)]
                if facing == 0:
                    print(">", end="")
                    continue
                if facing == 1:
                    print("V", end="")
                    continue
                if facing == 2:
                    print("<", end="")
                    continue
                if facing == 3:
                    print("^", end="")
                    continue

            if grid[y][x] == NONEXIST:
                print(" ", end="")
                continue
            
            print(grid[y][x], end="")
    print()

def parse_input(data):
    with open(data) as f:
        row_input = f.read().splitlines()
        controls = row_input[-1]
        del row_input[-1]

        grid = [[],[]]
        grid_map = {}
        max_y = len(row_input)
        max_x = 0
        max_x = max([len(row) for row in row_input])

        grid = [[NONEXIST for x in range(max_x)] for y in range(max_y)]

        for y, row in enumerate(row_input):
            for x, value in enumerate(row):
                if value != " ":
                    grid[y][x] = value
                    grid_map[(x+1, y+1)] = value
        return Cube(grid, grid_map), parse_controls(controls)

def parse_controls(controls_string):
    pattern = r"([A-Z])+"
    return re.split(pattern, controls_string)

def main():
    cube, controls = parse_input("input.txt")
    for x in range(cube.max_x):
        pos = (x + 1, 1)
        if pos in cube.grid_map and cube.check_grid(pos) != "#":
            start_pos = pos
            break
    player = Player(start_pos)

    for action in controls:
        if not action.isdigit():
            player.rotate(action)
        else:
            steps = int(action)
            for _ in range(steps):
                pos, next_pos = player.move()
                next_facing = player.facing
                direction = player.facing
                if next_pos not in cube.grid_map:
                    next_pos, next_facing = cube.stitch_map[(pos, direction)]

                if cube.check_grid(next_pos) == "#":
                    player.set_pos(pos)
                else:
                    player.set_pos(next_pos)
                    player.set_direction(next_facing)
    
    # 1000 * row + 4 * column + facing
    row = player.pos[1]
    column = player.pos[0]
    facing = player.facing
    answer_two = 1000 * row + 4 * column + facing
    print(answer_two) 

if __name__ == "__main__":
    main()
