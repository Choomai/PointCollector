from colorama import Fore
import colorama

colorama.init()
def logger(success: bool, uid, name):
    if success: print(f"{Fore.LIGHTGREEN_EX}Success | {uid} | {name}.{Fore.WHITE}")
    else: print(f"{Fore.LIGHTRED_EX}Failed | {uid} | {name}.{Fore.WHITE}")