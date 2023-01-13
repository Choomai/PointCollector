import PIL
from time import sleep
import pyautogui as pyui
sleep(1)
class cordinates:
    def __init__(self):
        self.loginbtn_x = 352
        self.loginbtn_y = 479
        self.uid_x = 284
        self.uid_y = 394
        self.passwd_x = 284
        self.passwd_y = 442
        self.name_st_x = 865
        self.name_st_y = 278
        self.name_en_x = 1015
        self.name_en_y = 278
        self.scr = 174,350,997,408
        self.scr_xy = 174,350,1171,758 # This is SCREEN cord, not correct args.
num_range = range(3000_000000,3000_999999)
print(num_range)
cord = cordinates()
pyui.write(str(3000_000000))
pyui.screenshot("./imgs/new_test.png",region=cord.scr)