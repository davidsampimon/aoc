
from copy import deepcopy


def parse_input(data):
    with open(data, "r") as f:
        input_list = f.read().splitlines()
    return [int(x) for x in input_list]

def shift_left(target, pos_dict):
    for index, posnum, in pos_dict.items():
        pos = posnum[0]
        value = posnum[1]

        if pos > target:
            pos -= 1        
        pos_dict[index] = (pos, value)
    return pos_dict

def shift_right(target, pos_dict):
    for index, posnum, in pos_dict.items():
        pos = posnum[0]
        value = posnum[1]

        if pos >= target:
            pos += 1        
        pos_dict[index] = (pos, value)
    return pos_dict

def mixing(original_list, n):
    position_map = {}
    for pos, value in enumerate(original_list):
        position_map[pos] = (pos, value)

    total_length = len(original_list)
    mix_list = deepcopy(original_list)
    for num in range(n):
        print(f"{num + 1}/{n}")
        for index in range(total_length):
            pos, value = position_map[index]
            target_index = (pos + value) % (total_length - 1)
            del mix_list[pos]
            position_map = shift_left(pos, position_map)
            mix_list.insert(target_index, value)
            position_map = shift_right(target_index, position_map)
            position_map[index] = (target_index, value)
    return mix_list


def main():
    original_list = parse_input("input.txt")
    mix_list = mixing(original_list, 1)
    start_index = mix_list.index(0)
    total_length = len(mix_list)
    index_x = (start_index + 1000) % total_length
    index_y = (start_index + 2000) % total_length
    index_z = (start_index + 3000) % total_length
    answer_one = mix_list[index_x] + mix_list[index_y] + mix_list[index_z]
    # Puzzle 1
    print(answer_one)

    # Puzzle 2
    decryption_key = 811589153
    decrypt_list = [num * decryption_key for num in original_list]

    mix_list_two = mix_list = mixing(decrypt_list, 10)    
    start_index = mix_list_two.index(0)
    index_x = (start_index + 1000) % total_length
    index_y = (start_index + 2000) % total_length
    index_z = (start_index + 3000) % total_length
    answer_two = mix_list[index_x] + mix_list[index_y] + mix_list[index_z]
    print(answer_two)

if __name__ == "__main__":
    main()