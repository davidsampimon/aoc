from dataclasses import dataclass
from functools import reduce
from collections import deque
import re


@dataclass
class Message:
    sender: str
    receiver: str
    signal: str


class Network:  # singleton
    __instance = None

    def __init__(self):
        if Network.__instance is not None:
            raise Exception(
                "You cannot create more than one instance of Network."
            )
        else:
            Network.__instance = self
        self.queue = deque()

    @staticmethod
    def get_instance():
        if Network.__instance is None:
            Network()
        return Network.__instance

    def send(self, message):
        self.queue.append(message)

    def process(self):
        return self.queue.popleft()


class ComMod:
    def __init__(self, destination_modules, key):
        self.input_modules = dict()
        self.destination_modules = destination_modules
        self.key = key
        self.network = Network.get_instance()

    def send(self, signal):
        for module in self.destination_modules:
            self.network.send(Message(self.key, module, signal))

    def get_inputs(self):
        return [(self.key, module) for module in self.destination_modules]

    def set_input(self, input):
        self.input_modules[input] = "Low"

    def reset(self):
        pass


class FlipFlop(ComMod):
    def __init__(self, destination_modules, key):
        super().__init__(destination_modules, key)
        self.state = False

    def reset(self):
        self.state = False

    def receive(self, message):
        match message.signal:
            case "High":
                return None
            case "Low":
                if self.state:
                    self.state = not self.state
                    self.send("Low")
                else:
                    self.state = not self.state
                    self.send("High")


class Conjunction(ComMod):
    def __init__(self, destination_modules, key):
        super().__init__(destination_modules, key)

    def receive(self, message):
        self.input_modules[message.sender] = message.signal
        if all(signal == "High" for signal in self.input_modules.values()):
            self.send("Low")
        else:
            self.send("High")

    def reset(self):
        for mod in self.input_modules.keys():
            self.input_modules[mod] = "Low"


class Broadcast(ComMod):
    def __init__(self, destination_modules, key):
        super().__init__(destination_modules, key)

    def receive(self, message):
        self.send(message.signal)


class Output(ComMod):
    def __init__(self, destination_modules, key):
        super().__init__(destination_modules, key)

    def receive(self, message):
        pass


def data(filepath):
    with open(filepath, "r") as f:
        lines = f.read().splitlines()

    mod_dict = dict()
    for line in lines:
        dirty_data = line.split("->")
        dest_mods = dirty_data[1].split(",")
        dest_mods = [name.strip() for name in dest_mods]
        if "output" in dest_mods:
            mod_dict["output"] = Output([], "output")
        if "broadcaster" in dirty_data[0]:
            mod_dict["broadcaster"] = Broadcast(dest_mods, "broadcaster")
        else:
            match dirty_data[0][0]:
                case "%":
                    name = re.search(r"(?<=\%)\S+", dirty_data[0]).group(0)
                    mod_dict[name] = FlipFlop(dest_mods, name)
                case "&":
                    name = re.search(r"(?<=\&)\S+", dirty_data[0]).group(0)
                    mod_dict[name] = Conjunction(dest_mods, name)
    return mod_dict


def p2_solver(network, modules, start):
    button_press = 0
    answer = dict()
    listen_for = modules["cl"].input_modules
    while True:
        network.send(start)
        button_press += 1
        while network.queue:
            message = network.process()
            if message.sender in listen_for and message.signal == "High":
                if not answer.get(message.sender):
                    answer[message.sender] = button_press
                if len(answer) == len(listen_for):
                    return reduce((lambda x, y: x * y), answer.values())

            if modules.get(message.receiver):
                modules[message.receiver].receive(message)


if __name__ == "__main__":
    modules = data("input.txt")
    network = Network.get_instance()

    # set inputs
    for module in modules.values():
        inputs = module.get_inputs()
        for sender, receiver in inputs:
            if modules.get(receiver):
                modules[receiver].set_input(sender)

    # Puzzle 1
    start = Message("button", "broadcaster", "Low")
    num = 1000

    count_low = 0
    count_high = 0
    for _ in range(num):
        network.send(start)
        while network.queue:
            message = network.process()
            if message.signal == "High":
                count_high += 1
            if message.signal == "Low":
                count_low += 1
            if modules.get(message.receiver):
                modules[message.receiver].receive(message)

    answer = count_low * count_high
    print(f"Answer 1: {answer}")

    # Puzzle 2
    for module in modules.values():
        module.reset()

    answer = p2_solver(network, modules, start)
    print(f"Answer 2: {answer}")
