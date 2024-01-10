import sys
sys.setrecursionlimit(10000000)


class Grid:
    def __init__(self, grid, size):
        self.map = grid
        self.heat_map = dict()
        self.size = size
        self.exit = (size[0]-1, size[1]-1)
        self.paths = list()
        self.min_heat_loss = 100000000

    def add(self, route):
        self.paths.append(route)

    def prune_out_of_bounds(self, options):
        results = list()
        while options:
            pos = options.pop(0)
            if not self.is_out_of_bounds(pos):
                results.append(pos)
        return results

    def is_out_of_bounds(self, pos):
        return (
            pos[0] < 0 or pos[0] >= self.size[0] or
            pos[1] < 0 or pos[1] >= self.size[1]
        )

    def prune_horizontals(self, pos, options):
        return [(opt[0], opt[1]) for opt in options if opt[0] != pos[0]]

    def prune_verticals(self, pos, options):
        return [(opt[0], opt[1]) for opt in options if opt[1] != pos[1]]

    # def find(self, pos, prev=(-1, 0), heat_loss=0, direction=(6, 7, 8)):      
    #     if self.heat_map.get(pos):
    #         if heat_loss < self.heat_map[pos]:
    #             self.heat_map[pos] = heat_loss
    #     else:
    #         self.heat_map[pos] = heat_loss

    #     options = neighbours(pos)
    #     options.remove(prev)
    #     options = self.prune_out_of_bounds(options)
    #     if len(set(direction)) == 1:
    #         match sum(direction):
    #             case 0:  # horizontal
    #                 options = self.prune_horizontals(pos, options)
    #             case 3:  # vertical
    #                 options = self.prune_verticals(pos, options)

    #     for option in options:
    #         new_direction = direction[1], direction[2], straight(pos, option)
    #         self.find(option, pos, heat_loss, new_direction)
        

    def search(self):
        while self.paths:
            route = self.paths.pop(0)
            if route.heat_loss > self.min_heat_loss:
                continue

            if route.pos == self.exit:
                self.min_heat_loss = min(route.heat_loss, self.min_heat_loss)

            if heat := self.heat_map.get(route.pos):
                self.heat_map[route.pos] = min(heat, route.heat_loss)
            else:
                self.heat_map[route.pos] = route.heat_loss


            route.heat_loss += self.map[route.pos]
            options = neighbours(route.pos)
            options = self.prune_out_of_bounds(options)
            options = [opt for opt in options if opt not in route.history]
            match route.straight_line():
                case "Horizontal":
                    options = self.prune_horizontals(options)
                case "Vertical":
                    options = self.prune_horizontals(options)
            for next_pos in options:
                self.paths.append(Route(next_pos, route.history[:], route.heat_loss))






    def draw(self, name="h"):
        match name:
            case "h":
                grid = self.heat_map

        for y in range(self.size[0]):
            print()
            for x in range(self.size[1]):
                print(grid[(y, x)], end="")
        print()


class Route:
    def __init__(self, pos, history=[None], heat_loss=0):
        self.pos = pos
        self.history = history
        self.heat_loss = heat_loss

    def move(self, pos):
        self.history.append(self.pos)
        self.pos = pos

    def straight_line(self):
        last_three = self.history[-3:]
        if len(last_three) < 3:
            return None

        tmp = list(zip(*last_three))
        if len(set(tmp[0])) == 1:  return "Horizontal"
        if len(set(tmp[1])) == 1:  return "Vertical"
        return None

def straight(pos, next):
    """
    horizontal = 0
    vertical = 1
    """
    if pos[0] == next[0]:
        return 1
    if pos[1] == next[1]:
        return 0


def neighbours(pos):
    return [
        (pos[0], pos[1] + 1),
        (pos[0] + 1, pos[1]),
        (pos[0], pos[1] - 1),
        (pos[0] - 1, pos[1]),
    ]


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

        grid = dict()
        height = len(lines)
        width = len(lines[0])

        for y, line in enumerate(lines):
            for x, heat_loss in enumerate(line):
                grid[(y, x)] = int(heat_loss)

        return Grid(grid, (height, width))

if __name__ == "__main__":
    grid = data("test.txt")
    grid.add(Route((0, 0)))

    grid.search()
    breakpoint()

    print(f"Answer 1: {grid.heat_map[grid.exit]}")

    print(grid.heat_map[(0, 1)])
    print(grid.heat_map[(0, 1)])
    print(grid.heat_map[(0, 2)])
    print(grid.heat_map[(1, 2)])
    print(grid.heat_map[(1, 3)])
    print(grid.heat_map[(1, 4)])
    print(grid.heat_map[(1, 5)])
    print(grid.heat_map[(0, 5)])
    print(grid.heat_map[(0, 6)])
    print(grid.heat_map[(0, 7)])
    print(grid.heat_map[(0, 8)])
    print(grid.heat_map[(1, 8)])
