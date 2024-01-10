from day21.puzzle import data


def split_range(func, rng):
    val = int(func[2:])
    match func[1]:
        case ">":
            true_range = (val + 1, rng[1])
            false_range = (rng[0], val)
        case "<":
            true_range = (rng[0], val - 1)
            false_range = (val, rng[1])
        case _:
            raise Exception(f"Unknown operator {func[1]} in {func}")
    return true_range, false_range


def is_valid(rng):
    return rng[0] <= rng[1]


class Machines:
    def __init__(self, machines):
        self.m = machines
        self.valid_ranges = list()

    @property
    def total_distincts(self):
        return sum([mchn.distinct for mchn in self.valid_ranges])

    def ranged_search(self, cm="in", ranges={
                "x": (1, 4000),
                "m": (1, 4000),
                "a": (1, 4000),
                "s": (1, 4000)
            }
    ):
        """
        cm - current machine name
        ranges - ranges for XMAS values
        """

        if cm == "A":
            self.valid_ranges.append(XMAS(ranges))
            return None

        if cm == "R":
            return None

        if sum(
            [(end - start) for start, end in ranges.values()]
        ) == 0:
            return None

        machine = self.m[cm]
        final = len(machine) - 1
        ranges = ranges.copy()
        for index, cmp in enumerate(machine):
            target = cmp[1]
            if index == final:
                return self.ranged_search(target, ranges.copy())

            func = cmp[0]
            key = func[0]
            rng = ranges[key]
            true_range, false_range = split_range(func, rng)

            # split off a branch for the true ranges
            if is_valid(true_range):
                true_rngs = ranges.copy()
                true_rngs[key] = true_range
                self.ranged_search(target, true_rngs)

            # continue without the split range
            if is_valid(false_range):
                ranges[key] = false_range
        return None


class XMAS:
    def __init__(self, ranges):
        self.x = ranges["x"]
        self.m = ranges["m"]
        self.a = ranges["a"]
        self.s = ranges["s"]
        self.distinct = self._calc_distinct()

    def __repr__(self):
        return f"{self.x}{self.m}{self.a}{self.s}"

    def _calc_distinct(self):
        lengthx = 1 + self.x[1] - self.x[0]
        lengthm = 1 + self.m[1] - self.m[0]
        lengtha = 1 + self.a[1] - self.a[0]
        lengths = 1 + self.s[1] - self.s[0]
        return lengthx * lengtha * lengthm * lengths


if __name__ == "__main__":
    tst, parts = data("test.txt")
    test = Machines(tst)
    test.ranged_search()
    assert 167409079868000 == test.total_distincts

    mchns, parts = data("input.txt")
    machines = Machines(mchns)
    machines.ranged_search()
    print(f"Answer 2: {machines.total_distincts}")
