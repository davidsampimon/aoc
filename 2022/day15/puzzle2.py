import re
from math import ceil, floor

GRID_SIZE = (0, 4000000)

class Line:
    def __init__(self, pos1, pos2):
        if pos1[0] <= pos2[0]:
            self.left = pos1
            self.right = pos2
        else:
            self.left = pos2
            self.right = pos1
    
    @property
    def coords(self):
        return (self.left, self.right)

class Sensor:
    def __init__(self, coord, beacon_pos):
        self.x = coord[0]
        self.y = coord[1]
        self.beacon_x = beacon_pos[0]
        self.beacon_y = beacon_pos[1]
        self.perimeter = []
        self._post_init()

    def _post_init(self):
        perim = self.distance + 1
        east = (self.x + perim + 1, self.y)
        south = (self.x, self.y + perim)
        west = (self.x - perim, self.y)
        north = (self.x, self.y - perim)

        self.perimeter.append(Line(east, south))
        self.perimeter.append(Line(south, west))
        self.perimeter.append(Line(west, north))
        self.perimeter.append(Line(north, east))

    @property
    def distance(self):
        return abs(self.x - self.beacon_x) + abs(self.y - self.beacon_y)

    def __repr__(self):
        return f"Sensor({self.x, self.y}, {self.beacon_x, self.beacon_y})"

def line_intersection(line1, line2):
    # Line1 represented as a1x + b1y = c1
    a1 = line1.right[1] - line1.left[1]
    b1 = line1.left[0] - line1.right[0]
    c1 = a1*(line1.left[0]) + b1*(line1.left[1])
 
    # Line2 represented as a2x + b2y = c2
    a2 = line2.right[1] - line2.left[1]
    b2 = line2.left[0] - line2.right[0]
    c2 = a2*(line2.left[0]) + b2*(line2.left[1])
 
    determinant = a1*b2 - a2*b1
 
    if (determinant == 0):
        # The lines are parallel.
        return False
    else:
        x = (b2*c1 - b1*c2)/determinant
        y = (a1*c2 - a2*c1)/determinant
        return (x, y)


def distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

def is_covered(pos, sensor_list):
    if on_map(pos):
        for sensor in sensor_list:
            if distance(pos, (sensor.x, sensor.y)) <= sensor.distance:
                return True
    return False

def on_map(pos):
    if not pos:
        return False
    min_x = GRID_SIZE[0]
    max_x = GRID_SIZE[1]
    min_y = GRID_SIZE[0]
    max_y = GRID_SIZE[1]

    return min_x <= pos[0] <= max_x and min_y <= pos[1] <= max_y

def frequency(pos):
    return pos[0] * 4000000 + pos[1]

def parse_input(data):
    input_list = []
    with open(data, "r") as f:
        for line in f:
            result = (re.findall(r'-?\d+\.?\d*', line))
            input_list.append([int(x) for x in result])

    result_list = []
    for row in input_list:
        sensor_pos = (row[0], row[1])
        beacon_pos = (row[2], row[3])
        result_list.append(Sensor(sensor_pos, beacon_pos))
    return result_list

if __name__ == "__main__":
    sensor_list = parse_input("input.txt")
    line_list = []
    results = set()
    for sensor1 in sensor_list:
        perimeter = sensor1.perimeter
        for sensor2 in sensor_list:
            if sensor1 == sensor2:
                continue
            for line1 in perimeter:
                for line2 in sensor2.perimeter:
                    intersect = (line_intersection(line1, line2))
                    if on_map(intersect):
                        results.add(intersect)

    for pos in results:
        x_floor_y_ceil = (floor(pos[0]), ceil(pos[1]))
        x_ceil_y_floor = (ceil(pos[0]), floor(pos[1]))
        if not is_covered(x_floor_y_ceil, sensor_list):
            print(frequency(x_floor_y_ceil))
        if not is_covered(x_ceil_y_floor, sensor_list):
            print(frequency(x_ceil_y_floor))