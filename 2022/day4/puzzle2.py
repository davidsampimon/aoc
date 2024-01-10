import csv
from day5.puzzle1 import parse_row

def is_intersect(partner_one, partner_two):
    set1 = set(partner_one)
    set2 = set(partner_two)
    if len(set1.intersection(set2)) > 0:
        return True
    return False

if __name__ == "__main__":
    partner_overlap = 0

    with open("input.txt", "r") as f:
        csv_file = csv.reader(f)
        for index, row in enumerate(csv_file):
            partner_one, partner_two = parse_row(row)
            if is_intersect(partner_one, partner_two):
                partner_overlap += 1
                print(f"{partner_overlap}: line: {index + 1} - {partner_one} {partner_two}")

    print(partner_overlap)