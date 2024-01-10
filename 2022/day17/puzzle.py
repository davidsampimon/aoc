import heapq
import itertools

ROCK_TYPES = [
    [
        ["#","#","#","#"]
    ],
    [
        [".","#","."],
        ["#","#","#"],
        [".","#","."]
    ],
    [
        [".",".","#"],
        [".",".","#"],
        ["#","#","#"]
    ],
    [
        ["#"],
        ["#"],
        ["#"],
        ["#"]
    ],
    [
        ["#","#"],
        ["#","#"]
    ]
]

def parse_input(data):
    with open(data, "r") as f:
        data_string = f.read().strip()
    return itertools.cycle(data_string)

class Controller:
    def __init__(self, data):
        self.string_buffer = data

    def next_input(self):
        return next(self.string_buffer)

class RockProducer:
    def __init__(self, rocks=ROCK_TYPES):
        self.rocks = rocks
        self.count = 0
    
    def next_rock(self):
        length = len(self.rocks)
        rock = self.rocks[self.count]
        self.count = (self.count + 1) % length
        return rock

class Chamber:
    def __init__(self, rockproducer, height, width):
        self.rockproducer = rockproducer
        self._grid_init(height, width)
        self.rock_pos = (-1, -1)
        self.rock_counter = 0
        self.new_rock()
        self.collision_map = []
    
    def _grid_init(self, height, width):
        self.grid = [["." for x in range(width)] for y in range(height)]

    @property
    def y(self):
        return len(self.grid)
    
    @property
    def x(self):
        return len(self.grid[0])

    @property
    def collision(self):
        return [
            (self.rock_pos[0] - pos[0], pos[1] + self.rock_pos[1])
             for pos in self.rock_collision
            ]
    
    def move(self, action):
        match action:
            case ">":
                self._move_right()
                self._move_down()
            case "<":
                self._move_left()
                self._move_down()
    
    def _move_right(self):
        right_edge = self.rock_pos[1] + (len(self.rock[0]) - 1)
        if right_edge + 1 >= self.x:
            return
        for pos in self.collision:
            if (pos[0]*-1, pos[1] + 1) in self.collision_map:
                return
        self.rock_pos = (self.rock_pos[0], self.rock_pos[1] + 1)

    def _move_left(self):
        if self.rock_pos[1] - 1 < 0:
            return
        for pos in self.collision:
            if (pos[0] * -1, pos[1] - 1) in self.collision_map:
                return
        self.rock_pos = (self.rock_pos[0], self.rock_pos[1] - 1)

    def _move_down(self):
        if self.is_free():
            self.rock_pos = (self.rock_pos[0] - 1, self.rock_pos[1])
        else:
            self._draw_rock()
            self.add_rock(self.collision)
            self.new_rock()
        
    def is_free(self):
        bottom = min([pos[0] for pos in self.collision])
        if bottom == 0:
            return False
        for pos in self.collision:
            if ((pos[0] - 1)*-1, pos[1]) in self.collision_map:
                return False
        return True

    def add_rock(self, collision):
        for pos in collision:
            heapq.heappush(self.collision_map, (pos[0]*-1, pos[1]))

    def new_rock(self):
        self.rock = self.rockproducer.next_rock()
        self.rock_counter += 1
        peak = self.peak_rock()
        if peak:
            new_peak = peak[0] + len(self.rock) + 4
        else:
            new_peak = len(self.rock) + 3

        if new_peak > self.y:
            for _ in range(new_peak - self. y):
                self.grid.append(
                    ["." for x in range(self.x)]
            )
        self.rock_pos = ((new_peak - 1), 2)
        self.set_rock_collision()

    def set_rock_collision(self):
        self.rock_collision = []
        for y in range(len(self.rock)):
            for x in range(len(self.rock[0])):
                if self.rock[y][x] == "#":
                    self.rock_collision.append((y,x))
    
    def _draw_rock(self):
        for pos in self.collision:
            self.grid[pos[0]][pos[1]] = "#"

            
    def _remove_rock(self):
        for pos in self.collision:
            self.grid[pos[0]][pos[1]] = "."
    
    def draw(self):
        self._draw_rock()
        for y in range((self.y-1), -1, -1):
            print()
            for x in range(self.x):
                print(self.grid[y][x], end="")
        print()
        self._remove_rock()

    def peak_rock(self):
        for y in range(self.y -1, -1, -1):
            for x in range(self.x):
                if self.grid[y][x] == "#":
                    return (y, x)


def main(input_file):
    string_buffer = parse_input(input_file)
    controller = Controller(string_buffer)
    rocks = RockProducer()
    chamber = Chamber(rocks, 1, 7)
    while chamber.rock_counter < 2023 :
        # chamber.draw()
        chamber.move(controller.next_input())
    result = chamber.peak_rock()[0] + 1
    print(result)



if __name__ == "__main__":
    main("input.txt")
