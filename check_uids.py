import re
from extension import read_env
config = read_env()
for index in config:
    try: 
        config[index] = int(config[index])
        continue
    except ValueError: pass

    try: 
        config[index] = bool(config[index])
        continue
    except ValueError: pass
missing = []

with open("./collected/ctt/UIDs and names.txt", "r", encoding="utf-8") as f:
    ids = re.findall(r"[0-9]{10}", f.read())
    ids = [int(elem) for elem in ids]
    
    for i in range(config["ctt_start_UID"], config["ctt_end_UID"]):
        if not config["ctt_start_UID"] <= i < config["ctt_end_UID"]: missing.append(i)

with open("./collected/ctt/missing.txt", "w", encoding="utf-8") as f_miss:
    f_miss.write(str(missing))