import requests
from dotenv import dotenv_values
from bs4 import BeautifulSoup
import lxml
from lxml.html.clean import Cleaner
from minify_html import minify
import json
import re
import colorama
import backoff
from colorama import Fore
from time import sleep

config = dotenv_values(".env")
for index in config:
    try: 
        config[index] = int(config[index])
        continue
    except ValueError: pass

    try: 
        config[index] = bool(config[index])
        continue
    except ValueError: pass
def logger(success: bool, uid, name, status: int):
    if success: print(f"{Fore.LIGHTGREEN_EX}Success | {status} | {uid} | {name}.{Fore.WHITE}")
    else: print(f"{Fore.LIGHTRED_EX}Failed | {status} | {uid} | {name}.{Fore.WHITE}")
def clean_attrib(html_str: str):
    cleaner = Cleaner(safe_attrs_only=True, safe_attrs=frozenset({"class", "id"})) # Add the remove_empty_space parameter
    return cleaner.clean_html(minify(html_str.replace("<td>:</td>", ""), keep_closing_tags=True))
@backoff.on_exception (backoff.expo, requests.exceptions.Timeout, max_time=60)
def make_request(url: str, params):
    response = requests.get(url, timeout=60, params=params, headers=headers)
    return response

colorama.init()
headers = {"User-Agent": f"python-requests/{requests.__version__} (PointCollector/{config.app_ver}; +https://fallback.choomai.xyz/bots/collector.txt)"}
ts10_url = "http://khaothi.thuathienhue.edu.vn:8080/tracuu/chitietthcs.html"

for id in range(config["ts10_start_ID"], config["ts10_end_ID"]):
    req = make_request(ts10_url, params={"id": id})
    html = BeautifulSoup(clean_attrib(req.text), "lxml")

    table = html.find(lambda tag: tag.name == "table" and "KẾT QUẢ THI" in tag.text).tr.td.div.table
    table.select_one("tr:first-child > td:last-child").decompose()
    name = table.select_one("tr:first-child > td:last-child").text

    data = {}
    tr_list = table.find_all("tr")
    for tr in tr_list:
        td_list = tr.find_all("td")
        key, val = td_list[0].text, td_list[1].text

        if key == "Số báo danh":
            data[key] = int(data[key])
            continue
        try: data[key] = float(data[key])
        except ValueError: continue
        data[key] = val

    if name:
        with open(f"./collected/ts10/{id}_{name}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4) # Write the dictionary object to the JSON file
            logger(True, id, name, req.status_code)
    else: logger(False, id, name, req.status_code)