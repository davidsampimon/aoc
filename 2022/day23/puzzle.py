from collections import deque

from profiler import profile

cache = {}

def get_neighbors(pos):
    if pos in cache:
        return cache[pos]
    x = pos[0]
    y = pos[1]
    cache[pos] = {
        "N": (x, y-1) ,
        "S": (x, y+1),
        "W": (x-1, y),
        "E": (x+1, y),
        "NE": (x+1, y-1),
        "NW": (x-1, y-1),
        "SE": (x+1, y+1),
        "SW": (x-1, y+1)
    }
    return cache[pos]

class ElfGroup:
    def __init__(self, elf_list):
        self.elf_list = set(elf_list)
        self.total_elves = len(elf_list)
        self.propose_map = {}
        self.search_order = deque([
            ("N", ["N", "NE", "NW"]),
            ("S", ["S", "SE", "SW"]),
            ("W", ["W", "NW", "SW"]),
            ("E", ["E", "NE", "SE"])
        ])

    def first_half(self):
        """
        If no other Elves are in one of those eight positions, the Elf does not do anything during this round. Otherwise,
        If there is no Elf in the N, NE, or NW adjacent positions, the Elf proposes moving north one step.
        If there is no Elf in the S, SE, or SW adjacent positions, the Elf proposes moving south one step.
        If there is no Elf in the W, NW, or SW adjacent positions, the Elf proposes moving west one step.
        If there is no Elf in the E, NE, or SE adjacent positions, the Elf proposes moving east one step.
        """
        self.propose_map = {}
        stable_counter = 0
        for pos in self.elf_list:
            neighbors = get_neighbors(pos)
        
            if self.is_empty(neighbors.values()):
                stable_counter += 1
                if stable_counter == self.total_elves:
                    raise Exception("No moves left")
                continue
            prio_count = 1

            for rule in self.search_order:
                key = rule[0]
                # print(f"Prio {prio_count}: {elf}@{key}")
                prio_count += 1
                wd = rule[1]
                check_list = [
                    neighbors[wd[0]],
                    neighbors[wd[1]],
                    neighbors[wd[2]]
                ]
                if self.is_empty(check_list):
                    self.update_propose_map(neighbors[key], pos)
                    break
        # rotate search order
        self.search_order.rotate(-1)

    def second_half(self):
        for new_pos, pos in self.propose_map.items():
            if not pos:
                continue
            self.elf_list.remove(pos)
            self.elf_list.add(new_pos)


    def update_propose_map(self, pos, elf):
        if pos in self.propose_map:
            self.propose_map[pos] = None
        else:
            self.propose_map[pos] = elf

    def is_empty(self, check_list):
        return not any([pos in self.elf_list for pos in check_list])


def parse_input(data):
    with open(data, "r") as f:
        row_input = f.read().splitlines()

    elf_list = []
    for y, row in enumerate(row_input):
        for x, value in enumerate(row):
            if value == "#":
                elf_list.append((x, y))
    return elf_list

def draw(elfgroup):
    elves = elfgroup.elf_list
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0

    for pos in elves:
        min_x = min(min_x, pos[0])
        max_x = max(max_x, pos[0])
        min_y = min(min_y, pos[1])
        max_y = max(max_y, pos[1])

    width = max_x - min_x
    height = max_y - min_y
    empty_counter = 0

    for y in range(height + 1):
        print()
        for x in range(width + 1):
            pos = (x + min_x, y + min_y)
            if pos in elves:
                print("#", end="")
            else:
                print(".", end="")
                empty_counter += 1
    print()
    return empty_counter


def main():
    elf_list = parse_input("input.txt")
    elves = ElfGroup(elf_list)
    
    # Puzzle 1
    rounds = 10
    for round in range(rounds):
        print(round + 1)
        elves.first_half()
        elves.second_half()

    empty_counter = draw(elves)
    # Answer puzzle 1
    print(empty_counter)

    # Puzzle 2
    elves_two = ElfGroup(elf_list)
    round = 1
    while True:
        try:
            elves_two.first_half()
        except Exception:
            # Answer puzzle 2
            print(f"Answer puzzle 2: {round}")
            break
        elves_two.second_half()
        round += 1
    


if __name__ == "__main__":
    main()
