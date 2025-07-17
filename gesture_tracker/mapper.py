import csv

def build_mapping_from_csv(file_path):
    mapping = {}
    current_virtual_id = 0

    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start = int(row['Entity Start'])
            end = int(row['Entity End'])

            for real_id in range(start, end + 1):
                mapping[current_virtual_id] = real_id
                current_virtual_id += 1

    return mapping
