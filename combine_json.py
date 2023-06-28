import json
import glob
import csv
from tqdm import tqdm

json_dir = input("Enter the path of JSON files: ")
output_format = int(input("0 == JSON | 1 == CSV\nChoose one: "))
need_convert = bool(input("Convert keys that are text to number (True|False) ? "))

data = []
json_files = glob.glob(json_dir + '/*.json')

for file_name in tqdm(json_files):
    with open(file_name, 'r', encoding='utf-8') as f:
        file_data = json.load(f)
        if need_convert:
            for key in file_data.keys():
                if key == "Số báo danh": 
                    file_data[key] = int(file_data[key])
                    continue
                try: file_data[key] = float(file_data[key])
                except ValueError: continue
        data.append(file_data)

if output_format == 0:
    with open('combined.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
elif output_format == 1:
    keys = data[0].keys()
    with open('combined.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)