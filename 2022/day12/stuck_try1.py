class Point():
    def __init__(self, coord, territory):
        self.y = coord[0]
        self.x = coord[1]
        self.options = []
        self.map = territory
        self.analyze()

    @property
    def height(self):
        return self.map[self.y][self.x]
    
    def analyze(self):
        down = (self.y+1, self.x)
        up = (self.y-1, self.x)
        left = (self.y, self.x-1)
        right = (self.y, self.x+1)

        if self._test(down):
            self.options.append(down)
        if self._test(up):
            self.options.append(up)
        if self._test(left):
            self.options.append(left)
        if self._test(right):
            self.options.append(right)
    
    def _test(self, coord):
        breakpoint()
        if self.map.on_map(coord):
            if self.map.is_possible((self.y, self.x), coord):
                return True
        return False


    

class Territory:
    def __init__(self, line_list):
        self.map = line_list
        self.grid_y = len(line_list)
        self.grid_x = len(line_list[0])
        self.start_position, self.end_position = self._find_start_end()
        self.position = self.start_position
        self.history = []

    def _find_start_end(self):
        for y in range(0, self.grid_y):
            for x in range(0, self.grid_x):
                if self.map[y][x] == "S":
                    start_position = (y, x)
                if self.map[y][x] == "E":
                    end_position = (y, x)
        return Point(start_position, self.map), Point(end_position, self.map)

    @property
    def route_length(self):
        return len(set(self.history))

    def on_map(self, coord):
        y = coord[0]
        x = coord[1]
        if x or y < 0:
            return False
        if y > self.grid_y:
            return False
        if x > self.grid_x:
            return False
        return True

    def is_possible(self, from_coord, to_coord):
        from_height = self.map[from_coord[0]][from_coord[1]]
        to_height = self.map[to_coord[0]][to_coord[1]]
        return (from_height - to_height) >= -1

    def route(self, route_list):
        for option in self.position.options:
            if option == self.end_position:
                return route_list
            if option in self.history:
                continue
            new_point = Point(option, self.map)
            self.history.append(option)
            self.position = new_point
            breakpoint()
            self.route(route_list)


if __name__ == "__main__":
    with open("input.txt", "r") as f:
        total_lines = f.read().splitlines()

    territory = Territory(total_lines)
    breakpoint()
