import sys
from collections import deque

from profiler import profile

sys.setrecursionlimit(1000000)

def manhatten_distance(start_pos, end_pos):
    return abs(end_pos[0] - start_pos[0]) + abs(end_pos[1] - start_pos[1])

def positions(pos):
    y = pos[0]
    x = pos[1]
    return [
        (y, x),
        (y, x+1),
        (y+1, x),
        (y, x-1),
        (y-1, x)
    ]

class DGrid:
    def __init__(self, grid, depth):
        self.grid_data = grid
        self.collision_map = grid.collision_map
        self.depth = depth
        self.grid = [[[]]]
        self._init_grid()
    
    def _init_grid(self):
        depth = self.depth
        height = self.grid_data.height
        width = self.grid_data.width

        grid = [[[-1 for x in range(width)]for y in range(height)]for d in range(depth)]

        for z in range(depth):
            state = z % self.grid_data.max_maps
            for y in range(height):
                for x in range(width):
                    if (y, x) in self.collision_map[state]:
                        grid[z][y][x] = "#"
        self.grid = grid

    def bfs_two(self, pos, to_pos, count=0, steps_found=1000000):
        if count >= self.depth:
            return

        if steps_found:
            if count > steps_found:
                return

        if self.grid[count][pos[0]][pos[1]] == -1:
            self.grid[count][pos[0]][pos[1]] == count
        
        next_state = (count + 1) % self.grid_data.max_maps
        options = set(positions(pos)) - self.collision_map[next_state]
        for pos_ in options:
            if pos_ == to_pos:
                steps_found = min(count + 1, steps_found)

            if self.grid[next_state][pos_[0]][pos_[1]] == -1:
                self.grid[next_state][pos_[0]][pos_[1]] = count + 1
                self.bfs_two(pos_, to_pos, count + 1, steps_found)
            
            if self.grid[next_state][pos_[0]][pos_[1]] > count + 1:
                self.grid[next_state][pos_[0]][pos_[1]] = count + 1
                self.bfs_two(pos_, to_pos, count + 1, steps_found)

    def search_answer(self, from_pos, to_pos, count=0):
        answers = []
        self.bfs_two(from_pos, to_pos, count=count)
        depth = self.depth
        for z in range(depth):
            if self.grid[z][to_pos[0]][to_pos[1]] != -1:
                answers.append(self.grid[z][to_pos[0]][to_pos[1]])
        return min(answers)


class Grid:
    def __init__(
        self, start, end, height, width, wall, north, east, west, south):
        self.start = start
        self.end = end
        self.height = height
        self.width = width
        self.max_maps = height * width
        self.wall_map = wall
        self.north_map = north
        self.east_map = east
        self.west_map = west
        self.south_map = south
        self.collision_map = {}
        self._init_collision_maps()
    
    def _init_collision_maps(self):
        for map_num in range(self.max_maps):
            self.collision_map[map_num] = set(self.wall_map)
            self.collision_map[map_num].update(
                [
                    (self.start[0] - 1, self.start[1]),
                    (self.end[0] + 1, self.end[1])
                ]
                )
            self.collision_map[map_num].update(
                self.directions_update("N", map_num))
            self.collision_map[map_num].update(
                self.directions_update("E", map_num))
            self.collision_map[map_num].update(
                self.directions_update("W", map_num))
            self.collision_map[map_num].update(
                self.directions_update("S", map_num))

    def directions_update(self, direction, n):
        match direction:
            case "N":
                return [
                    ((pos[0] - 1 - n) % (self.height - 2) + 1, pos[1] ) for pos in self.north_map
                ]
            case "E":
                return [
                    (pos[0], (pos[1] - 1 + n) % (self.width - 2) + 1 ) for pos in self.east_map
                ]
            case "W":
                return [
                    (pos[0], (pos[1] - 1 - n) % (self.width - 2) + 1 ) for pos in self.west_map
                ]                
            case "S":
                return [
                    ((pos[0] - 1 + n) % (self.height - 2) + 1, pos[1] ) for pos in self.south_map
                ]
    
    @profile
    def bfs(self, round):
        visited = {}
        queue = deque([(self.start, round)])
        max_state = self.width * self.height
        end_steps = 10000000

        while queue:
            pos, round = queue.popleft()
            # distance = manhatten_distance(pos, self.end)
            if end_steps > round:
                state = round % max_state
                next_map = (round + 1) % max_state
                if (pos, state) not in visited:
                    visited[(pos, state)] = round
                if pos not in self.collision_map[state]:
                    if round <= visited[(pos, state)]:
                        visited[(pos, state)] = round
                        options = set(
                            positions(pos)
                            ) - self.collision_map[next_map]
                        for pos_ in options:
                            if pos_ == self.end:
                                end_steps = round + 1
                            # if self.on_map(pos_):
                            queue.append((pos_, round + 1))
        return [end_steps, visited]

    def on_map(self, pos):
        return 0 <= pos[0] < self.height and 0 <= pos[1] < self.width

def parse_input(data):
    with open(data, "r") as f:
        row_input = f.read().splitlines()
        height = len(row_input)
        width = len(row_input[0])
        wall_map = set()
        north_map = set()
        east_map = set()
        west_map = set()
        south_map = set()

        for y, row in enumerate(row_input):
            for x, value in enumerate(row):
                if y == 0:
                    if value != "#":
                        start = (y, x)
                if y == height - 1:
                    if value == ".":
                        end = (y, x)
                match value:
                    case "#":
                        wall_map.add((y, x))
                    case "^":
                        north_map.add((y, x))
                    case ">":
                        east_map.add((y, x))
                    case "<":
                        west_map.add((y, x))
                    case "v":
                        south_map.add((y, x))

        return Grid(
            start,
            end,
            height,
            width,
            wall_map,
            north_map,
            east_map,
            west_map,
            south_map
        )




def main():
    grid = parse_input("input.txt")
    d_grid = DGrid(grid, 10000)
    # from s to e
    answer_one = d_grid.search_answer(
        d_grid.grid_data.start,
        d_grid.grid_data.end
        )
    
    d_grid._init_grid()
    # from e to s
    mid_time = d_grid.search_answer(
        d_grid.grid_data.end,
        d_grid.grid_data.start,
        count=answer_one)
    answer_two = mid_time - answer_one
    d_grid._init_grid()
    # from s to e
    total_time = d_grid.search_answer(
        d_grid.grid_data.start,
        d_grid.grid_data.end,
        count=mid_time)
    answer_three = total_time - answer_two - answer_one
    print(total_time)
    breakpoint()



if __name__ == "__main__":
    main()
