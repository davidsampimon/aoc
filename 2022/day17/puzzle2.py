import time
import heapq
from copy import deepcopy
from collections import deque

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
    return data_string.strip()

class Controller:
    def __init__(self, data):
        self.string_buffer = data
        self.len = len(data)
        self.count = 0

    def next_input(self):
        action = self.string_buffer[self.count]
        self.count = (self.count + 1) % self.len
        return action

class RockProducer:
    def __init__(self, rocks=ROCK_TYPES):
        self.rocks = rocks
        self.count = 0
        self.rock_collisions = []
        self.set_rock_collisions()
    
    def next_rock(self):
        length = len(self.rock_collisions)
        collision_map = self.rock_collisions[self.count]
        rock_type = self.count
        self.count = (self.count + 1) % length
        return rock_type, collision_map
    
    def collisions(self, rock):
        collision_map = []
        for y in range(len(rock)):
            for x in range(len(rock[0])):
                if rock[y][x] == "#":
                    collision_map.append((y,x))
        return collision_map

    def set_rock_collisions(self):
        for rock in self.rocks:
            self.rock_collisions.append(self.collisions(rock))


class Chamber:
    def __init__(self, rockproducer, controller, width):
        self.width = width
        self.rockproducer = rockproducer
        self.controller = controller
        self.rock_pos = (-1, -1)
        self.collision_map = []
        self.round = {
            "rock_type" : 0,
            "pos": (0, 0),
            "input": ""
        }
        self.round_counter = 0
        self.new_rock()

    @property
    def y(self):
        return max(self.peak_rock(), max([pos[0] for pos in self.collision]))
    
    @property
    def x(self):
        return self.width

    @property
    def collision(self):
        return [
            (self.rock_pos[0] - pos[0], pos[1] + self.rock_pos[1])
             for pos in self.rock_collision
            ]
    
    def peak_rock(self):
        smallest = heapq.nsmallest(1, self.collision_map)
        if smallest == []:
            return -1
        return smallest[0][0] * - 1
    
    def move(self, action):
        self.round["input"] += action
        match action:
            case ">":
                self._move_right()
                self._move_down()
            case "<":
                self._move_left()
                self._move_down()

    def play_round(self):
        round = self.round_counter
        self.round = {
            "rock_type" : 0, # 2
            "xpos": (0),  #  4
            "input": ""   # >>><
        }
        while self.round_counter == round:
            self.move(self.controller.next_input())

    def _move_right(self):
        right_edge = max([pos[1] for pos in self.collision])
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
            self.add_rock()
            self.new_rock()
        
    def is_free(self):
        for pos in self.collision:
            if ((pos[0] - 1)*-1, pos[1]) in self.collision_map:
                return False
        bottom = min([pos[0] for pos in self.collision])
        if bottom == 0:
            return False
        return True

    def add_rock(self):
        self.round["pos"] = self.rock_pos[1]
        self.round["rock_type"] = self.rock_type
        self.round_counter += 1
        if len(self.collision_map) > 100:
            self.collision_map = self.collision_map[-100:] + [
                (pos[0]*-1, pos[1]) for pos in self.collision
            ]
        else:
            self.collision_map = self.collision_map + [
                (pos[0]*-1, pos[1]) for pos in self.collision
            ]

    def new_rock(self):
        self.rock_type, self.rock_collision = self.rockproducer.next_rock()
        peak = self.peak_rock()
        new_peak = peak + max([pos[0] for pos in self.rock_collision]) + 5
        self.rock_pos = ((new_peak - 1), 2)

    def draw(self):
        for y in range(self.y, -1, -1):
            print()
            for x in range(self.x):
                if (y*-1, x) in self.collision_map:
                    print("#", end="")
                elif (y, x) in self.collision:
                    print("#", end="")
                else:
                    print(".", end="")
        print()

def main(input_file):
    # set-up
    string_buffer = parse_input(input_file)
    controller = Controller(string_buffer)
    rocks = RockProducer()
    puzzle_one = Chamber(rocks, controller, 7)
    hare = Chamber(deepcopy(rocks), deepcopy(controller), 7)
    tortoise = Chamber(deepcopy(rocks), deepcopy(controller), 7)

    # Puzzle 1
    check_num = 2022
    while puzzle_one.round_counter < check_num:
        puzzle_one.play_round()

    answer_one = puzzle_one.peak_rock() + 1
    print(f"Answer puzzle 1: {answer_one}")

    # Puzzle 2
    check_num = 1000000000000
    tortoise_history = {}
    hare_nrounds = deque(5*"", 5)
    tortoise_nrounds = deque(5*"", 5)
    while tortoise.round_counter < check_num :
        # play H twice for T once
        hare.play_round()
        hare_nrounds.append(hare.round)
        hare.play_round()
        hare_nrounds.append(hare.round)
        tortoise.play_round()
        tortoise_nrounds.append(tortoise.round)
        tortoise_history[tortoise.round_counter] = (
            tortoise.peak_rock() + 1
        )
        if tortoise_nrounds == hare_nrounds:
            print("Loop found")
            tortoise_height = tortoise.peak_rock() + 1
            hare_height = hare.peak_rock() + 1
            print(
                f"Tortoise: round {tortoise.round_counter}, " 
                f"height {tortoise_height} \n"
                f"Hare: round {hare.round_counter}, "
                f"height {hare_height}"
            )

            cycle_length = hare.round_counter - tortoise.round_counter
            cycle_height = hare_height - tortoise_height
            start_offset = tortoise_height
            total_cycles = (
                (check_num - (tortoise.round_counter ))
                ) // cycle_length
            rem_rounds = (
                (check_num - (tortoise.round_counter ))
                ) % cycle_length
            break

    answer_two = (
        start_offset + 
        total_cycles * cycle_height + 
        tortoise_history[rem_rounds + 1]
    )

    print(f"Answer puzzle 2: {answer_two}")

    

if __name__ == "__main__":
    start_time = time.time()
    main("test.txt")
    end_time = time.time()
    res = end_time - start_time
    print('Execution time:', res, 'seconds')
