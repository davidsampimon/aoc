import re


LOOKUP_ORDER = [
    "seed-to-soil",
    "soil-to-fertilizer",
    "fertilizer-to-water",
    "water-to-light",
    "light-to-temperature",
    "temperature-to-humidity",
    "humidity-to-location"
]


Puzzle 2

SeedRanges
(2, 4), (6, 8), (10, 2)





Layers
(10, 8) => (30, 8)
(20, 5) => (50, 5)


intersect((2, 4), (10, 8))


# ----            self
#   ----------    other

(3, 1)

class SeedRange():
    def __init__(self, start, length):
        self.start = start
        self.length = length

    @property
    def end(self):
        return self.start + self.length

    def __repr__(self):
        return f"({self.start}, {self.length})"

    def intersect(self, other):
        start = max(self.start, other.start)
        length = min(self.end, other.end) - start
        if length <= 0:
            return None
        return SeedRange(start, length)

    def transpose(self, shift):
        self.start = self.start + shift

    def split(self, other):
        inter = self.intersect(other)

        if inter is None:
            # ---      inter
            #      --- self
            return [SeedRange(self.start, self.length)]
        elif (self.start, self.length) == (inter.start, inter.length):
            # ---      inter
            # ---      self
            return []
        elif inter.start == self.start:
            # ---      inter
            # ------   self
            start = inter.end
            length = self.end - inter.end
            return [SeedRange(start, length)]
        elif inter.end == self.end:
            #   -----  inter
            # -------  self
            return [SeedRange(self.start, inter.start - self.start)]
        else:
            #   --     inter
            # -------  self
            return [
                SeedRange(self.start, inter.start - self.start),
                SeedRange(inter.end, self.end - inter.end)
            ]


class SeedMap(SeedRange):
    def __init__(self, start, length, trnsps):
        super().__init__(start, length)
        self.shift = trnsps

    def __lt__(self, other):
        return self.start < other.start


class Maps():
    def __init__(self, seedmap_list):
        self.maps = seedmap_list
        self.maps.sort(key=lambda map: map.start)


class Solver():
    def __init__(self, maps):
        self.maps = maps
        self.answer = int(10000000000)

    def traverse(self, rng, layer=0):
        if layer == len(LOOKUP_ORDER):
            self.answer = min(self.answer, rng.start)
            return self.answer

        m_name = LOOKUP_ORDER[layer]
        for mp in self.maps[m_name]:
            inter = rng.intersect(mp)

            if inter:
                inter.transpose(mp.shift)
                self.traverse(inter, layer+1)
                sub = rng.split(mp)
                if len(sub) == 0:
                    return
                rng = sub[0]
                if len(sub) == 2:
                    self.traverse(sub[1], layer)
        self.traverse(rng, layer+1)


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    dirty_seeds = re.findall(r"\d+", lines.pop(0))

    seeds = list()
    for num in range(len(dirty_seeds) // 2):
        seed_start = int(dirty_seeds[num * 2])
        length = int(dirty_seeds[(num * 2) + 1])
        seeds.append(SeedRange(seed_start, length))

    maps = {}
    for line in lines:
        if "map:" in line:
            dict_key = line.replace(" map:", "")
            maps[dict_key] = []
        elif line == "":
            pass
        else:
            dirty_nums = re.findall(r"\d+", line)
            source_start = int(dirty_nums[1])
            destination_start = int(dirty_nums[0])
            trnsps = destination_start - source_start
            length = int(dirty_nums[2])

            maps[dict_key].append(
                SeedMap(source_start, length, trnsps)
            )

    return maps, seeds


if __name__ == "__main__":
    maps, seeds = data("input.txt")

    # ten_two = SeedRange(10, 2)
    # two_to = SeedRange(2, 2)
    # eight_five = SeedRange(8, 5)
    # eight_f = SeedRange(8, 5)
    # eight_two = SeedRange(8, 2)
    # ten_three = SeedRange(10, 3)
    # fif_fif = SeedRange(50, 50)

    p2 = Solver(maps)

    for seed in seeds:
        p2.traverse(seed)

    print(f"Answer 2: {p2.answer}")
