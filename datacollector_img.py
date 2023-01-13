import PIL
import win32clipboard as clipboard
from time import sleep
import pyautogui as pyui
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
        self.name_en_x = 1030
        self.name_en_y = 278
        self.scr = 174,350,997,418
        self.scr_xy = 174,350,1171,768 # This is SCREEN cord, not correct args.
        self.logoutbtn_x = 1148
        self.logoutbtn_y = 280
# num_range = range(3000_350000,3000_400000)
num_range = range(3000_350193,3000_400000)
cord = cordinates()
sleep(3)
print("Script is active.")
for i in num_range:
    sleep(2)
    pyui.click(x = cord.uid_x, y = cord.uid_y)
    sleep(0.1)
    pyui.write(str(i), 0.05)
    pyui.click(x = cord.passwd_x, y = cord.passwd_y)
    sleep(0.1)
    pyui.write("cc", 0.01)
    sleep(0.1)
    pyui.click(x = cord.loginbtn_x, y = cord.loginbtn_y)
    # End login
    sleep(2.5)
    pyui.moveTo(cord.name_st_x,cord.name_st_y)
    pyui.dragTo(cord.name_en_x,cord.name_en_y,1,button="left")
    pyui.hotkey("ctrl","c",interval=0.1)
    # End name copy
    clipboard.OpenClipboard()
    clip_data = clipboard.GetClipboardData().replace(" ","")
    if (len(clip_data) > 45 or clip_data == "notthis"):
        pyui.click(x = cord.logoutbtn_x, y = cord.logoutbtn_y)
        clipboard.CloseClipboard()
        continue
    clipboard.SetClipboardText("notthis")
    clipboard.CloseClipboard()

    pyui.screenshot(f"./imgs/{i}_{clip_data}.png", region=cord.scr)
    # End screenshot
    pyui.click(x = cord.logoutbtn_x, y = cord.logoutbtn_y)
    # End logout