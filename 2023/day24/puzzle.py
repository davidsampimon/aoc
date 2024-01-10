import itertools
import math
from collections import namedtuple


Hail = namedtuple("Hail", ["x", "y", "z", "dx", "dy", "dz"])



def find_pos_and_velo(stones, component):
    max_val = 400
    min_result = 5
    for dx in range(-1*max_val, max_val):
        for dy in range(-1*max_val, max_val):
            dv = (dx, dy)
            matching_pos = set()
            count = 0
            
            processPairs(stones, component, deltaV) { intersection ->
                if (intersection != null) {
                    matchingPositions += intersection
                    resultCount++
                    resultCount < minResultCount
                } else {
                    false
                }
            }
            // We need exactly 1 position with at least minResultCount matches
            if (matchingPositions.size == 1 && resultCount >= min(minResultCount, stones.size / 2)) {
                return matchingPositions.single() to -deltaV
            }
        }
    }
    return null
}






def multiply(hail, num):
    x, y, z, dx, dy, dz = hail

    return (
        x + dx * num,
        y + dy * num,
        z + dz * num
    )

def within(pos, test_square):
    x, y = pos
    lower = test_square["min"]
    higher = test_square["max"]
    return all([
        (lower <= x <= higher),
        (lower <= y <= higher)
    ])

class Line:
    def __init__(self, pos1, pos2):
        self.pos1 = pos1
        self.pos2 = pos2
    
    def __repr__(self):
        return f"({self.pos1}, {self.pos2})"

    @property
    def angle(self):
        x1, y1, z1 = self.pos1
        x2, y2, z2 = self.pos2
        m = (y2 - y1) / (x2 - x1)
        theta = math.atan(m)
        return math.degrees(theta)

    def cross(self, other):
        inter = self.intersect(other)
        if not inter:
            return None

        if self.valid(self, inter) and self.valid(other, inter):
            return inter
        else:
            return None

    @staticmethod
    def valid(line, inter):
        x1, y1, z1 = line.pos1
        x2, y2, z2 = line.pos2
        x_set = {
            (x1 - x2) < 0,
            (x1 - inter[0]) < 0
        }
        y_set = {
            (y1 - y2) < 0,
            (y1 - inter[1]) < 0

        }
        return len(x_set) == 1 and len(y_set) == 1


    def intersect(self, other):
        x1, y1, z1 = self.pos1
        x2, y2, z2 = self.pos2
        x3, y3, z3 = other.pos1
        x4, y4, z4 = other.pos2
        m1 = (y2 - y1) / (x2 - x1)
        m2 = (y4 - y3) / (x4 - x3)
        if m1 == m2:
            return None
        b1 = y1 - m1 * x1
        b2 = y3 - m2 * x3
        x = (b2 - b1) / (m1 - m2)
        y = m1 * x + b1
        return x, y


def data(filepath):
    with open(filepath) as f:
        lines = f.read().splitlines()

    hail_list = list()
    for line in lines:
        pos, velo = line.split("@")
        x, y, z = [int(i) for i in pos.split(",")]
        dx, dy, dz = [int(i) for i in velo.split(",")]
        hail_list.append(
            Hail(x, y, z, dx, dy, dz)
        )
    return hail_list


if __name__ == "__main__":
    hail_stones = data("test.txt")
    lines = [
        Line(
            (hail.x, hail.y, hail.z),
            (hail.x + hail.dx, hail.y + hail.dy, hail.z + hail.dz)
        ) for hail in hail_stones
        ]

    # Puzzle 1
    test_square = {
        "min": 200000000000000,
        "max": 400000000000000
    }
    count = 0
    for line_a, line_b in itertools.combinations(lines, 2):
        inter = line_a.cross(line_b)
        if inter:
            if within(inter, test_square):
                count += 1
    print(f"Answer 1: {count}")

    # Puzzle 2
    frames = len(hail_stones)
    hail_map = list()
    frame_num = 0
    while lin_find:
        frame_num += 1
        hail_map.append([multiply(hail, frame_num) for hail in hail_stones])
    pass
