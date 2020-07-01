import csv
# from itertools import zip_longest
import filecmp

# row_A = ['pccn', 'plisn', 'cfi', 'item_name', 'unit_price', 'failure_rate']
# len_A = [6, 5, 1, 12, 8, 8]
# row_B= ['pccn', 'plisn', 'cfi', 'next_higher_plisn', 'qty_per_assembly', 'blank']
# len_B = [6, 5, 1, 5, 5, 18]
mcolumns = ['pccn', 'plisn', 'item_name', 'unit_price', 'failure_rate','next_higher_plisn', 'qty_per_assembly']


with open('lsa_multi_line.txt', 'r') as f:
    mvalues = []
    d = {}
    for i, line in enumerate(f.readlines()):

        if i % 2 == 0:
            # A line
            d = {}
            d['pccn'] = line[0:6].strip()
            d['plisn'] = line[6:11].strip()
            d['item_name'] = line[12:23].strip()
            d['unit_price'] = line[23:31].strip()
            d['failure_rate'] = line[31:40].strip()
        else:
            # B line
            d['next_higher_plisn'] = line[12:17].strip()
            d['qty_per_assembly'] = line[17:22].strip()
            mvalues.append(d)

with open("res_lsa_multi_line_parsed.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, mcolumns)
    writer.writeheader()

    for d in mvalues:
        writer.writerow(d)

fc = filecmp.cmp('res_lsa_multi_line_parsed.csv', 'lsa_multi_line_parsed.csv')
print(f"lsa_multi_line_parsed File Comparison {fc}")
