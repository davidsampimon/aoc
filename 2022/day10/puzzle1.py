class Cpu:
    def __init__(self, signal_list):
        self.signal_list = signal_list
        self.x = 1
        self.cycle_count = 0
        self.busy = False

    def cycle(self, count):
        self.cycle_count = count

    def noop(self):
        pass

    def addx(self, x):
        self.x += x
    
    def signal_strength(self, i):
        if i in self.signal_list:
            return i * self.x
        return 0
    
    def draw_pixel(self, i):
        current_pixel = (i - 1) % 40
        if current_pixel == 0:
            print()
        x_list = [self.x - 1, self.x, self.x +1]
        if current_pixel in x_list:
            print("#", end="")
        else:
            print(".", end="")


if __name__ == "__main__":
    cpu = Cpu([20, 60, 100, 140, 180, 220])
    execution_dict = {}

    with open("input.txt", "r") as f:
        total_lines = f.read().splitlines()

    cycle_count = 0
    for line in total_lines:
        match line.split()[0]:
            case "noop":
                cycle_count += 1
                execution_dict[cycle_count] = "noop"
            case "addx":
                (x_in) = line.split()[1]
                cycle_count += 2
                execution_dict[cycle_count] = "addx", int(x_in)

    max_cycles = max(execution_dict.keys())

    signal_strength = 0
    print("Puzzle 2:")
    for i in range(1, max_cycles + 1):
        signal_strength += cpu.signal_strength(i)
        cpu.draw_pixel(i)
        if i in execution_dict.keys():
            action = execution_dict[i]
            if "addx" in action:
                cpu.addx(action[1])
    print()
    print(f"Puzzle 1: {signal_strength}")
