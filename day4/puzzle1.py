import csv

def parse_row(dirty_row):
    partner_one = get_sections(dirty_row[0])
    partner_two = get_sections(dirty_row[1])
    return partner_one, partner_two

def get_sections(section_input):
    start_section, end_section = section_input.split("-")
    return range(int(start_section), (int(end_section) + 1)) 

def is_subset(partner_one, partner_two):
    return set(partner_one).issubset(partner_two)

if __name__ == "__main__":
    partner_overlap = 0

    with open("input.txt", "r") as f:
        csv_file = csv.reader(f)
        for index, row in enumerate(csv_file):
            partner_one, partner_two = parse_row(row)
            if is_subset(partner_one, partner_two) or is_subset(partner_two, partner_one):
                partner_overlap += 1
                print(f"{partner_overlap}: line: {index + 1} - {partner_one} {partner_two}")

    print(partner_overlap)
