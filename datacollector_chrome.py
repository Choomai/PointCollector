from selenium import webdriver
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
colorama.init()
driver = webdriver.Chrome()
def login(inp_uid):
    driver.get("https://qlttgddt.thuathienhue.edu.vn/home/dangnhap.aspx")
    uid = driver.find_element(By.ID, "txtUser")
    uid.send_keys(inp_uid)
    passwd = driver.find_element(By.ID, "txtPass")
    passwd.send_keys("cc") # Anything will work...
    login_btn = driver.find_element(By.ID, "btnDangNhap")
    login_btn.send_keys(Keys.ENTER)
def table_sel(num, semester): # (1..10, 1 or 2) | 1st is current year, 2nd is the next,... ; Semester 1 or 2
    _class = driver.find_element(By.XPATH, f"//select[@id='ctl05_drpNamHoc']/option[{str(num)}]") # 2021-2022 (if first option is 2022-2023)
    _class.click()
    sems = driver.find_element(By.XPATH, f"//select[@id='ctl05_drpHocKy']/option[{str(semester)}]")
    sems.click()
def clean_attrib(html_str):
    # Ignore common attrib maybe ? https://stackoverflow.com/questions/7470333/remove-certain-attributes-from-html-tags
    cleaner = clean.Cleaner(safe_attrs_only=True, safe_attrs=frozenset({'colspan'}))
    return cleaner.clean_html(html_str)
def logout():
    btn = driver.find_element(By.ID, "LinkButton2")
    btn.click()
# user_id = 3000_350_000
for user_id in range(3000350000,3000400000): # UID range
    login(user_id)
    table_sel(2,1)
    name_raw = driver.find_element(By.XPATH,"//*[@id='lblTenTaiKhoan']/span").get_attribute('outerHTML')
    name = BeautifulSoup(name_raw, "lxml").string
    if name == "": name = "noname"
    table = driver.find_element(By.XPATH, "//span[@id='ctl05_lblDanhSach']/table")

    table_raw = clean_attrib(minify_html.minify(table.get_attribute('outerHTML'), keep_closing_tags=True))
    table = BeautifulSoup(table_raw, "lxml")

    table_head = table.tr.extract()
    table_head.name = "thead"
    for elem in table_head.find_all("td"): elem.name = "th" # Replace all td with th

    table_body = table.tbody.extract()
    table.table.append(table_head)
    table.table.append(table_body)
    str_cond = table_body.td.string

    df = pd.read_html(str(table))
    df_json = df[0].to_json(orient='records', force_ascii=False, indent=4)
    if (str_cond == "Chưa cập nhật môn học") or (str_cond == "Học sinh chưa được phép xem kết quả học tập Học kỳ 1") or (str_cond == "Học sinh chưa được phép xem kết quả học tập Học kỳ 2"):
        print(f"{Fore.LIGHTRED_EX}Skipped UID {user_id} with the name {name}{Fore.WHITE}.")
    else: 
        with open(f"./collected/{str(user_id)}_{name}.json", "w", encoding="utf-8") as file:
            file.write(df_json)
            file.close()
            print(f"{Fore.LIGHTGREEN_EX}Finished writing UID {user_id} with the name {name}.")
    logout()
sleep(10)