import requests
from dotenv import dotenv_values
from bs4 import BeautifulSoup
import lxml
from lxml.html.clean import Cleaner
from minify_html import minify
import json
import re
import colorama
from colorama import Fore
from time import sleep

config = dotenv_values(".env")
for index in config:
    if not config[index] in ["true", "false"]: config[index] = int(config[index])
    elif config[index] == "true": config[index] = True
    elif config[index] == "false": config[index] = False
def logger(success: bool, uid, name, status: int):
    if success: print(f"{Fore.LIGHTGREEN_EX}Success | {status} | {uid} | {name}.{Fore.WHITE}")
    else: print(f"{Fore.LIGHTRED_EX}Failed | {status} | {uid} | {name}.{Fore.WHITE}")
def clean_attrib(html_str: str):
    cleaner = Cleaner(safe_attrs_only=True, safe_attrs=frozenset({"class", "id"})) # Add the remove_empty_space parameter
    return cleaner.clean_html(minify(html_str.replace("<td>:</td>", ""), keep_closing_tags=True))

colorama.init()
headers = {"User-Agent": f"python-requests/{requests.__version__} (PointCollector/1.2; +https://fallback.choomai.xyz/bots/collector.txt)"}
ts10_url = "http://khaothi.thuathienhue.edu.vn:8080/tracuu/chitietthcs.html"

for id in range(config["ts10_start_ID"], config["ts10_end_ID"]):
    req = requests.get(ts10_url, params={"id": id}, headers=headers)
    if req.status_code == 429:
        print("Got an 429, waiting for 1m server cooldown.")
        sleep(60)
        id -= 1
        continue
    html = BeautifulSoup(clean_attrib(req.text), "lxml")

    table = html.find(lambda tag: tag.name == "table" and "KẾT QUẢ THI" in tag.text).tr.td.div.table
    table.select_one("tr:first-child > td:last-child").decompose()
    name = table.select_one("tr:first-child > td:last-child").text

    data = {}
    tr_list = table.find_all("tr")
    for tr in tr_list:
        td_list = tr.find_all("td")
        data[td_list[0].text] = td_list[1].text
    
    if name:
        with open(f"./collected/ts10/{id}_{name}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4) # Write the dictionary object to the JSON file
            file.close()
            logger(True, id, name, req.status_code)
    else: logger(False, id, name, req.status_code)