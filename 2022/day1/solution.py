from collections import Counter

total_cals = Counter()
elf_index = 0

with open("input.csv", "r") as f:
    for row in f:
        cleaned_row = row.strip()
        if cleaned_row == "":
            elf_index += 1
        else:
            total_cals[elf_index] += int(cleaned_row)
print("Answer puzzle 1")
print(f"highest cal_count: {max(total_cals.values())}")

N = 3 
top_results = sorted(total_cals.values(), reverse=True)[0:N]
print("Answer puzzle 2")
print(f"Total of top three: {sum(top_results)}")