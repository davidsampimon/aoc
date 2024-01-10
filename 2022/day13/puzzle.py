import ast
from copy import deepcopy
from functools import cmp_to_key


def compare(left, right):
    match left, right:
        case int(left), int(right): return compare_ints(left, right)
        case list(left), int(right): return compare(left, [right])
        case int(left), list(right): return compare([left], right)
        case list(left), list(right):
            for result in map(compare, left, right):
                if result: return result
            return compare(len(left), len(right))

def compare_ints(left, right):
    return (left > right) - (left < right)
    
def parse_input(data):
    packet_list = []
    result = []
    with open(data, "r") as f:
        for row in f:
            line = row.strip()
            if line == "":
                result = []
                continue
            parsed_line = ast.literal_eval(line)
            result.append(parsed_line)
            if len(result) == 2:
                packet_list.append(deepcopy(result))
    return packet_list


if __name__ == "__main__":
    packet_list = parse_input("input.txt")

    ## Puzzle 1
    answer = 0
    for index, packet in enumerate(packet_list, 1):
        result = compare(packet[0], packet[1])
        if result == -1:
            answer += index
    print(answer)

    ## Puzzle 2
    extra_packets = sum(packet_list, [[[2]],[[6]]])
    sorted_packets = sorted(extra_packets, key=cmp_to_key(compare))
    x = sorted_packets.index([[2]])
    y = sorted_packets.index([[6]])
    print(x*y)
