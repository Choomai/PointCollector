import json
import glob
from tqdm import tqdm

json_dir = input("Enter the path of JSON files: ")
json_files = glob.glob(json_dir + '/*.json')


for file_name in tqdm(json_files):
    with open(file_name, 'r', encoding='utf-8') as f: data = json.load(f)

    for key in data.keys():
        if key == "Số báo danh": 
            data[key] = int(data[key])
            continue
        try: data[key] = float(data[key])
        except ValueError: continue

    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
