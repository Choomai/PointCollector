from dotenv import dotenv_values
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import minify_html
import lxml
import lxml.html.clean as clean
import pandas as pd
import colorama
import sys
from colorama import Fore
from time import sleep

config = dotenv_values(".env")
for index in config:
    if not config[index] in ["true", "false"]: config[index] = int(config[index])
    elif config[index] == "true": config[index] = True
    elif config[index] == "false": config[index] = False

def login(inp_uid):
    uid = driver.find_element(By.ID, "txtUser")
    uid.send_keys(inp_uid)
    passwd = driver.find_element(By.ID, "txtPass")
    passwd.send_keys("cc") # [CONFIG] Anything will work...
    login_btn = driver.find_element(By.ID, "btnDangNhap")
    login_btn.send_keys(Keys.ENTER)
def table_sel(num, semester):
    driver.find_element(By.XPATH, f"//select[@id='ctl05_drpNamHoc']/option[{str(num)}]").click()
    driver.find_element(By.XPATH, f"//select[@id='ctl05_drpHocKy']/option[{str(semester)}]").click()
def clean_attrib(html_str):
    cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=frozenset({'colspan'})) # Keep 'colspan' safe.
    return cleaner.clean_html(html_str)
def logout(): driver.find_element(By.ID, "LinkButton2").click()
def logger(success: bool, uid, name):
    if success: print(f"{Fore.LIGHTGREEN_EX}Success | {uid} | {name}.{Fore.WHITE}")
    else: print(f"{Fore.LIGHTRED_EX}Failed | {uid} | {name}.{Fore.WHITE}")

colorama.init()
chrome_options = Options()
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--log-level=3") 
chrome_options.add_argument("--disable-extension")
chrome_options.add_argument("--disable-in-process-stack-traces")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://qlttgddt.thuathienhue.edu.vn/home/dangnhap.aspx")
file_name = open("./collected/ctt/UIDs and names.txt", "a", encoding="utf-8")

for user_id in range(config["ctt_start_UID"], config["ctt_end_UID"]):
    # 1. Login and fetch table.
    login(user_id)
    table_sel(config["year"], config["semester"])
    table = driver.find_element(By.XPATH, "//span[@id='ctl05_lblDanhSach']/table")
    table_raw = clean_attrib(minify_html.minify(table.get_attribute('outerHTML'), keep_closing_tags=True))
    table = BeautifulSoup(table_raw, "lxml")

    # 2. Extract table header and correct it.
    table_head = table.tr.extract()
    table_head.name = "thead"
    for elem in table_head.find_all("td"): elem.name = "th"

    # 3. Extract table body and re-append both back to table.
    table_body = table.tbody.extract()
    table.table.append(table_head)
    table.table.append(table_body)

    # 4. Identify table
    str_cond = table_body.td.string
    name_raw = driver.find_element(By.XPATH,"//span[@id='lblTenTaiKhoan']/span").get_attribute('outerHTML')
    name = BeautifulSoup(name_raw, "lxml").string

    # 5. If table is valid, write it to /collected/ctt/{UID}_{Name}.json, else skip.
    
    if name is not None: file_name.write(str(user_id) + " - " + name + "\n")
    else: file_name.write(str(user_id) + " - null\n")
    if "--name-only" not in sys.argv:
        if str_cond in ["Chưa cập nhật môn học", "Học sinh chưa được phép xem kết quả học tập Học kỳ 1", "Học sinh chưa được phép xem kết quả học tập Học kỳ 2"]:
            logger(False, user_id, name)
        else:
            with open(f"./collected/ctt/{user_id}_{name}.json", "w", encoding="utf-8") as file:
                df = pd.read_html(str(table))
                df_json = df[0].to_json(orient='records', force_ascii=False, indent=4)
                file.write(df_json)
                file.close()
                logger(True, user_id, name)
    else: logger(True, user_id, name)
    logout()
file_name.close()
sleep(10)