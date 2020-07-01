import csv
from itertools import zip_longest
import filecmp


chunk = 0
columns = []
sizes = []

with open('lsa_single_line_def.csv', 'r') as format_f:
    for d in csv.DictReader(format_f):
        sizes.append(int(d['Column Width']))
        columns.append(d['Name'])
        chunk += int(d['Column Width'])


# TODO 'merge' Read and Write loops into one loop
# so there is no need to keep value_list

value_list = []
with open("lsa_single_line.txt", "r", newline='') as f:
    for i, line in enumerate(f.readlines()):
        values = []
        start = 0
        for ll in sizes:
            end = start + ll
            values.append(line[start:end].strip())
            start = end

        obj = dict(zip_longest(columns, values, fillvalue=''))
        value_list.append(obj)

with open("res_lsa_single_line_parsed.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, columns)
    writer.writeheader()

    for d in value_list:
        writer.writerow(d)

fc = filecmp.cmp('res_lsa_single_line_parsed.csv', 'lsa_single_line_parsed.csv')
print(f"File Comparison {fc}")
