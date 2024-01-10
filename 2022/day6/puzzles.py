def find_first_unique_signal(signal_string, unique_items):
    for end_num in range(0, len(signal_string)):
        start_num = end_num - unique_items
        if start_num < 0:
            continue
        if len(set(signal_string[start_num:end_num])) == unique_items:
            return end_num

with open("input.txt", "r") as f:
    signal_string = f.read().splitlines()[0]

print("# puzzle 1 #")
print(find_first_unique_signal(signal_string, 4))

print("# puzzle 2 #")
print(find_first_unique_signal(signal_string, 14))
