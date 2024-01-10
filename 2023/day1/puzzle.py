from re import finditer


def strip_chars(line):
    result = []
    for char in line:
        if char.isdigit():
            result.append(int(char))
    return result


def find_digits(line):
    result = []
    for index, char in enumerate(line):
        if char.isdigit():
            result.append((index, int(char)))
    return result


with open("input.txt", "r") as f:
    lines = f.readlines()

# puzzle 1
answer = 0
for line in lines:
    strip_line = strip_chars(line)
    first, last = strip_line[0], strip_line[-1]
    answer += int(str(first) + str(last))
print(f"Answer 1: {answer}")


# puzzle 2
number_list = [
    ("one", 1),
    ("two", 2),
    ("three", 3),
    ("four", 4),
    ("five", 5),
    ("six", 6),
    ("seven", 7),
    ("eight", 8),
    ("nine", 9),
]

answer = 0
found_numbers = []
for line in lines:
    digit_list = []
    for ptrn, repl in number_list:
        for match in finditer(ptrn, line):
            start, stop = match.span()
            digit_list.append((start, repl))
    digit_list += find_digits(line)
    found_numbers.append(sorted(digit_list))
    print(sorted(digit_list))

for row in found_numbers:
    cal_val = int(str(row[0][1]) + str(row[-1][1]))
    answer += cal_val

print(f"Answer 2: {answer}")
