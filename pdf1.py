import pyautogui as pag
import pyocr
from PIL import Image
import sys
import subprocess
import pyperclip
import os
import time

C_btn_x = 336
C_btn_y = 74

acr_path = '/Applications/Adobe Acrobat Reader.app/Contents/MacOS/AdobeReader'
td_path = "/Users/itschoolkanazawawest/OCR/todokede_data/"

td_list = sorted(os.listdir(td_path))

def name_position():
    pag.moveTo(1, 1)
    for count in range(50):
        try:
            position = pag.locateOnScreen('name.png')
            if position:
                print(f"Image found at: {position}")  # デバッグ出力
                return position
            else:
                raise Exception("Image not found")
        except Exception:
            time.sleep(1)
    raise Exception("Could not locate the image 'name.png' after 50 tries")

def calculate_name_w(x, w):
    end_x = 1075
    start_x = x + w
    NAME_W = end_x - start_x
    print(f"end_x: {end_x}, start_x: {start_x}, NAME_W: {NAME_W}")
    if NAME_W <= 0:
        raise ValueError(f"Calculated NAME_W is non-positive: {NAME_W}. Check the coordinates.")
    return NAME_W

def get_name_img(x, y, w, h, NAME_W):
    start_x = x + w
    start_y = y
    region = (start_x, start_y, NAME_W, h)
    print(f"Screenshot region: {region}")  # デバッグ出力
    try:
        name_img = pag.screenshot('temp.png', region=region)  # region を修正
        if not os.path.exists('temp.png'):
            raise IOError("Screenshot was not saved correctly.")
        return name_img
    except Exception as e:
        print(f"Failed to take screenshot: {e}")
        return None

if __name__ == '__main__':
    for idx, file in enumerate(td_list):
        print('open:', file)
        pdf_pro = subprocess.Popen([acr_path, td_path + file])
        time.sleep(5)  # PDFが開くまでの待機時間を十分に取る

        try:
            box = name_position()
            x, y, w, h = box.left, box.top, box.width, box.height
            print(f"Found image at: x={x}, y={y}, width={w}, height={h}")

            NAME_W = calculate_name_w(x, w)
            name_img = get_name_img(x, y, w, h, NAME_W)

            pag.click(C_btn_x, C_btn_y)
            time.sleep(1)

            if idx == 0:
                break
        except Exception as e:
            print(e)
