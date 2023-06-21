import json
import glob
import csv
from tqdm import tqdm

json_dir = input("Enter the path of JSON files: ")
output_format = int(input("0 == JSON | 1 == CSV\nChoose one: "))

data = []
json_files = glob.glob(json_dir + '/*.json')

for file_name in tqdm(json_files):
    with open(file_name, 'r', encoding='utf-8') as f:
        file_data = json.load(f)
        data.append(file_data)

if output_format == 0:
    with open('combined.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False)
elif output_format == 1:
    keys = data[0].keys()

    with open('combined.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)