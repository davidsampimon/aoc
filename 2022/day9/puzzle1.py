
class RopeEnds():
    def __init__(self, start_pos=(0, 0)):
        self.head_position = start_pos
        self.tail_position = start_pos
        self.head_history = [start_pos]
        self.tail_history = [start_pos]

    @property
    def unique_tail_positions(self):
        return len(set(self.tail_history))

    def _new_pos(self, pos):
        self.head_position = pos
        self.head_history.append(pos)
        self._check_tail()
        self.draw_frame()

    def move_right(self):
        y, x = self.head_position
        self._new_pos((y, x+1))
        
    def move_left(self):
        y, x = self.head_position
        self._new_pos((y, x-1))

    def move_up(self):
        y, x = self.head_position
        self._new_pos((y+1, x))
    
    def move_down(self):
        y, x = self.head_position
        self._new_pos((y-1, x))
    
    def _check_tail(self):
        y_diff = self.head_position[0] - self.tail_position[0]
        x_diff = self.head_position[1] - self.tail_position[1]
        if abs(y_diff) > 1:
            new_y = (self.head_position[0] + self.tail_position[0])//2
            new_x = self.head_position[1]
            self._change_tail_position((new_y, new_x))
        if abs(x_diff) > 1:
            new_x = (self.head_position[1] + self.tail_position[1])//2
            new_y = self.head_position[0]
            self._change_tail_position((new_y, new_x))

    def _change_tail_position(self, pos):
        self.tail_position = pos
        self.tail_history.append(pos)

    def draw_frame(self):
        y_h, x_h = self.head_position
        y_t, x_t = self.tail_position
        y_t = y_t - y_h
        x_t = x_t - x_h

        print(self.head_position)
        for y in range(-2, 3):
            for x in range(-2, 3):
                if y == 0 and x == 0:
                    print("H", end="")
                elif y == y_t and x == x_t:
                    print("T", end="")
                else:
                    print(".", end="")
            print()
        print("#####")


 
if __name__ == "__main__":
    with open("input.txt", "r") as f:
        total_lines = f.read().splitlines()

    rope_ends = RopeEnds(start_pos=(0, 0))

    for row in total_lines:
        cmd, total = row.split()
        total = int(total)
        match cmd:
            case "R":
                for _ in range(0, total):
                    rope_ends.move_right()
            case "L":
                for _ in range(0, total):
                    rope_ends.move_left()
            case "D":
                for _ in range(0, total):
                    rope_ends.move_down()
            case "U":
                for _ in range(0, total):
                    rope_ends.move_up()
    print("Answer puzzle1")
    print(rope_ends.unique_tail_positions)
