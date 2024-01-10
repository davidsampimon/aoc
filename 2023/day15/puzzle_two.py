from day18.puzzle import hash
import re

class Instruction():
    def __init__(self, label, operator, focal_length=None):
        self.operator = operator
        self.lens = Lens(label, focal_length)

    def __repr__(self):
        return f"{self.operator}: {self.lens}"


class Lens():
    def __init__(self, label, focal_length):
        self.label = label
        self.focal_length = focal_length
    
    def __eq__(self, other):
        if isinstance(other, Lens):
            return self.label == other.label
        return False

    def __repr__(self):
        if self.focal_length:
            return f"{self.label} {self.focal_length}"
        return f"Label: {self.label}, Op: {self.operator}"


def data(filepath):
    lens_list = list()
    with open(filepath, "r") as f:
        data_list = f.read().split(",")

    for instruction in data_list:
        label = re.search(r"^.*?(?=[-=])", instruction).group(0)
        operator = "=" if "=" in instruction else "-"
        if operator == "=":
            index = 1 + instruction.find("=")
            focal_length = instruction[index:]
            lens_list.append(
                Instruction(label, operator, int(focal_length))
            )
        else:
            lens_list.append(
                Instruction(label, operator)
            )

    return lens_list



if __name__ == "__main__":
    instructions = data("input.txt")

    boxes = [[] for _ in range(256)]

    for action in instructions:
        lens = action.lens
        box_num = hash(lens.label)
        content = boxes[box_num]
        match action.operator:
            case "-":
                if lens in content:
                    content.remove(lens)
            case "=":
                if content == []:
                    content.append(lens)
                else:
                    if lens in content:
                        index = content.index(lens)
                        del content[index]
                        content.insert(index, lens)
                    else:
                        content.append(lens)

    focusing_power = 0
    for box_num, box in enumerate(boxes):
        for slot, lens in enumerate(box):
            focusing_power += (box_num + 1) * (slot + 1) * lens.focal_length

    print(f"Answer 2: {focusing_power}")
