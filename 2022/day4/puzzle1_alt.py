import csv

def parse_row(dirty_row):
    partner_one = get_sections(dirty_row[0])
    partner_two = get_sections(dirty_row[1])
    return partner_one, partner_two

def get_sections(section_input):
    start_section, end_section = section_input.split("-")
    return [int(start_section), int(end_section)]

def wholly_contained(partner_one, partner_two) -> bool:
  """One range is fully within the other."""
  return (
    partner_one[0] <= partner_two[0] <= partner_two[1] <= partner_one[1] or partner_two[0] <= partner_one[0] <= partner_one[1] <= partner_two[1]
    )

if __name__ == "__main__":
    partner_overlap = 0

    with open("input.txt", "r") as f:
        csv_file = csv.reader(f)
        for index, row in enumerate(csv_file):
            partner_one, partner_two = parse_row(row)
            if wholly_contained(partner_one, partner_two):
                partner_overlap += 1

    print(partner_overlap)
