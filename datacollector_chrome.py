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
colorama.init()

chrome_options = Options()
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--log-level=3") # [CONFIG] Log levels. https://stackoverflow.com/questions/62137334/disable-console-output-of-webdriver-using-selenium-in-python
chrome_options.add_argument("--disable-extension")
chrome_options.add_argument("--disable-in-process-stack-traces")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://qlttgddt.thuathienhue.edu.vn/home/dangnhap.aspx")

for user_id in range(3000_350_000, 3000_400_000): # [CONFIG] UID range
    # 1. Login and fetch table.
    login(user_id)
    table_sel(1,1) # [CONFIG] Year ?, Semester 1 or 2
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

    # 5. If table is valid, write it to /collected/{UID}_{Name}.json, else skip.
    if (str_cond == "Chưa cập nhật môn học") or (str_cond == "Học sinh chưa được phép xem kết quả học tập Học kỳ 1") or (str_cond == "Học sinh chưa được phép xem kết quả học tập Học kỳ 2"):
        print(f"{Fore.LIGHTRED_EX}Skipped UID {user_id} with the name {name}.{Fore.WHITE}")
    else:
        with open(f"./collected/{user_id}_{name}.json", "w", encoding="utf-8") as file:
            df = pd.read_html(str(table))
            df_json = df[0].to_json(orient='records', force_ascii=False, indent=4)
            file.write(df_json)
            file.close()
            print(f"{Fore.LIGHTGREEN_EX}Finished writing UID {user_id} with the name {name}.{Fore.WHITE}")
    logout()
sleep(10)