import requests
from dotenv import dotenv_values
import json
import colorama
import backoff
from PIL import Image
import pytesseract
from io import BytesIO
import base64
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

def logger(success: bool, uid, status: int):
    if success: print(f"{Fore.LIGHTGREEN_EX}Success | {status} | {uid}.{Fore.WHITE}")
    else: print(f"{Fore.LIGHTRED_EX}Failed | {status} | {uid}.{Fore.WHITE}")


@backoff.on_exception (backoff.expo, requests.exceptions.Timeout, max_time=60)
def make_request(method: str, url: str, params = None):
    response = requests.request(method=method, url=url, timeout=60, params=params, headers=headers)
    return response

colorama.init()
headers = {
    'Accept': '*/*',
    'Accept-Language': 'vi-VN',
    'Connection': 'keep-alive',
    'Content-Type': 'application/json',
    'Dnt': '1',
    'Host': 'tracuudiem.thitotnghiepthpt.edu.vn',
    'Origin': 'http://tracuudiem.thitotnghiepthpt.edu.vn',
    'Referer': 'http://tracuudiem.thitotnghiepthpt.edu.vn/index.html',
    'Sec-Gpc': '1',
    # "User-Agent": f"python-requests/{requests.__version__} (PointCollector/1.3-beta; +https://fallback.choomai.xyz/bots/collector.txt)",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82',
}
payload = {
    "identifyNumber": None,
    "strCapcha": None,
    "sessionId": None
}
thptqg_result = "http://tracuudiem.thitotnghiepthpt.edu.vn/service/api/v1/lookup-scores"
thptqg_capcha = "http://tracuudiem.thitotnghiepthpt.edu.vn/service/api/v1/captcha"

for id in range(33002200, 33002201):
    attempt = 1
    while attempt <= config['max_attempts']:
        capcha_req = make_request("GET", thptqg_capcha)
        data = json.loads(capcha_req.text)

        payload['identifyNumber'] = str(id)
        payload['sessionId'] = data['data']['sessionId']

        decoded_image_data = base64.b64decode(data['data']['imageCaptcha'])

        text_img = Image.open(BytesIO(decoded_image_data)) # PNG text, hard to read.
        img = Image.new("RGBA", text_img.size, (255, 255, 255)) # Add white background, easier to read.
        img.paste(text_img, (0, 0), text_img)
        img.save("capcha.png")
        payload['strCapcha'] = pytesseract.image_to_string(img, config='-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789')[:5]

        result_req = requests.request("POST", thptqg_result, headers=headers, data=payload)
        result = result_req.json()
        if result['code'] >= 400:
            logger(False, id, result['code'])
            attempt += 1
            continue
        if result['code'] == 200:
            with open(f"./collected/thptqg/{id}.json", "w", encoding="utf-8") as file:
                json.dump(result, file, ensure_ascii=False, indent=4)
                logger(True, id, 200)
            break