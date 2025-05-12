from dotenv import dotenv_values
from colorama import Fore
import colorama

colorama.init()
def logger(success: bool, uid, name):
    if success: print(f"{Fore.LIGHTGREEN_EX}Success | {uid} | {name}.{Fore.WHITE}")
    else: print(f"{Fore.LIGHTRED_EX}Failed | {uid} | {name}.{Fore.WHITE}")

def read_env() -> list:
    config = dotenv_values(".env")
    for index in config.keys():
        try:
            config[index] = int(config[index])
            continue
        except ValueError: pass

        try: 
            config[index] = bool(config[index])
            continue
        except ValueError: pass
    return config