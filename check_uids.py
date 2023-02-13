import re
from dotenv import dotenv_values
config = dotenv_values(".env")
for index in config: 
    if not config[index] in ["true", "false"]: config[index] = int(config[index])
file_name = open("./collected/UIDs and names.txt", "r", encoding="utf-8")
ids = re.findall(r"[0-9]{10}",file_name.read())
ids = [int(elem) for elem in ids]
missing = []
for i in range(config["start_UIDs"], config["end_UIDs"]):
    if not config["start_UIDs"] <= i < config["end_UIDs"]: missing.append(i)
file_name_miss = open("./collected/missing.txt", "w", encoding="utf-8")
file_name_miss.write(str(missing))
file_name.close()
file_name_miss.close()