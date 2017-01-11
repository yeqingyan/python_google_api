import json
import csv

INPUT_FILE = "example.json"
OUTPUT_FILE = "example.csv"
headers = set()

input = json.load(open(INPUT_FILE))
for row in input:
    for item in input[row]:
        headers.add(item)
headers = list(headers)

f = open(OUTPUT_FILE, 'wb')
writer = csv.writer(f)
writer.writerow([""]+headers)

for row in input:
    output_row = [row]
    for item in headers:
        if item in input[row]:
            output_row.append("1")
        else:
            output_row.append("0")
    writer.writerow(output_row)

f.close

