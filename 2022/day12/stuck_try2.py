from operator import itemgetter
from dataclasses import field, dataclass


@dataclass
class Point:
    y: int
    x: int
    options: list()

class Territory:
    def __init__(self, lines_map):
        self.map = lines_map
        self.grid_y = len(lines_map)
        self.grid_x = len(lines_map[0])
        self.start_position, self.end_position = self._find_start_end()
        self.current_position = self.start_position
        self.history = []

    def _find_start_end(self):
        for y in range(0, self.grid_y):
            for x in range(0, self.grid_x):
                if self.map[y][x] == "S":
                    start_position = (y, x)
                if self.map[y][x] == "E":
                    end_position = (y, x)
        return self.analyze(start_position), self.analyze(end_position)

    def analyze(self, coord, preference=False):
        y = coord[0]
        x = coord[1]
        height = self.map[y][x]

        directions = [(y-1, x), (y+1, x), (y, x-1), (y, x+1)]

        if preference:
            directions = self.directions_preference(directions)

        options = self.options(height, directions)
        return Point(coord[0], coord[1], options)

    def options(self, height, directions):
        options = []
        for direction in directions:
            if self.is_on_map(direction):
                if self.is_possible(height, direction):
                    options.append(direction)
        return options

    def directions_preference(self, directions):
        results = {}
        for direction in directions:
            y_diff = direction[0] - self.end_position.y
            x_diff = direction[1] - self.end_position.x
            score = abs(y_diff) * abs(x_diff)
            results[score] = direction
        results = sorted(results.items(), key=itemgetter(0))
        index , direction = zip(*results)
        return direction

    
    def is_on_map(self, coord):
        y = coord[0]
        x = coord[1]

        if 0 <= y < self.grid_y:
            if 0 <= x < self.grid_x:
                return True
        return False

    def is_possible(self, from_height, coord):
        to_height = self.map[coord[0]][coord[1]]
        if from_height == "S":
            return True
        if to_height == "E":
            return from_height == "z"
        return ord(from_height) - ord(to_height) >= -1

    def move(self):
        if self.current_position == self.end_position:
            return self.history

        self.history.append(self.current_position)
        for position in self.current_position.options:
            option = self.analyze(position, preference=True)
            if option in self.history:
                continue
            self.current_position = option
            self.move()
            


if __name__ == "__main__":
    with open("sample.txt", "r") as f:
        total_lines = f.read().splitlines()

    territory = Territory(total_lines)

    results = None
    while not results:
        results = territory.move()

    for step in results:
        print((step.y, step.x))



