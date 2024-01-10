import re

class Player:
    def __init__(self):
        self.pos = (0, 0)
        # 0 = west, 1 = south, 2 = east, 3 = north
        self.facing = 0

    def set_pos(self, pos):
        self.pos = pos
    
    def _set_facing(self, facing):
        self.facing = (facing % 4)
    
    def rotate(self, action):
        match action:
            case "L":
                self._set_facing(self.facing - 1)
            case "R":
                self._set_facing(self.facing + 1)
            case _:
                raise Exception(f"Unknown action: {action}")
    
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

class Grid:
    def __init__(self, grid_map):
        self.grid_map = grid_map
        self.coords = self._init_coords()
    
    def start_pos(self):
        row = self.grid_map[0]
        for index, char in enumerate(row["grid"]):
            if char != "#":
                return ((index + row["start_offset"] + 1, 0 + 1))

    def on_map(self, coord):
        return coord in self.coords
    
    def move_logic(self, from_pos, to_pos):
        if self.on_map(to_pos):
            if self.check_coord(to_pos) == "#":
                return from_pos
            return to_pos
        
        wrap_pos = self.wrap_pos(from_pos, to_pos)
        return self.move_logic(from_pos, wrap_pos)
    
    def wrap_pos(self, from_pos, to_pos):
        delta_x = to_pos[0] - from_pos[0]
        delta_y = to_pos[1] - from_pos[1]

        wrap_pos = (from_pos[0] - delta_x, from_pos[1] - delta_y)
        while self.on_map(wrap_pos):
            wrap_pos = (wrap_pos[0] - delta_x, wrap_pos[1] - delta_y)
        
        return (wrap_pos[0] + delta_x, wrap_pos[1] + delta_y)


    def check_coord(self, coord):
        if self.on_map(coord):
            return self.coords[coord]
        else:
            return None

    def _init_coords(self):
        coord_map = {}
        for index, data in self.grid_map.items():
            y = index + 1
            offset = data["start_offset"]
            for index, char in enumerate(data["grid"]):
                x = index + offset + 1
                coord_map[(x, y)] = char
        return coord_map
    
    def draw(self):
        for row in self.grid_map.values():
            print()
            for _ in range(row["start_offset"]):
                print(" ", end="")
            for char in row["grid"]:
                print(char, end="")
        print()


def parse_input(data):
    with open(data, "r") as f:
        row_input = f.read().splitlines()
    
    controls = parse_controls(row_input[-1])
    del row_input[-1]
    grid_map = parse_grid(row_input)
    return grid_map, controls

def parse_controls(controls_string):
    pattern = r"([A-Z])+"
    return re.split(pattern, controls_string)

def parse_grid(dirty_grid):
    grid_map = {}

    for index, row in enumerate(dirty_grid):
        if len(dirty_grid) == 0:
            continue

        start_offset = 0
        for char in row:
            if char == " ":
                start_offset += 1
            else:
                break
        
        grid = row[start_offset:]
        grid_map[index] = {
            "start_offset" : start_offset,
            "grid" : grid
        }
    return Grid(grid_map)

def main():
    grid, controls = parse_input("input.txt")
    grid.draw()
    player = Player()
    player.set_pos(grid.start_pos())
    for action in controls:
        if not action.isdigit():
            player.rotate(action)
        else:
            for _ in range(int(action)):
                from_pos, to_pos = player.move()
                player.set_pos(grid.move_logic(from_pos, to_pos))
    
    # 1000 * row + 4 * column + facing
    row = player.pos[1]
    column = player.pos[0]
    facing = player.facing
    answer_one = 1000 * row + 4 * column + facing
    print(answer_one)

if __name__ == "__main__":
    main()
