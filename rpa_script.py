import pyautogui as pag
import pyocr
from PIL import Image
import sys
import subprocess

import pyperclip
import os
import time

CLOSE_BUTTON_X = 1881
CLOSE_BUTTON_Y = 15

acr_path = 'C:\Program Files (x86)\Adobe\Acrobat Reader DC\Reader\AcroRd32.exe'
todokede_path = 'todokede_data/'

todokede_list = os.listdir(todokede_path)

NAME_W = 206
WAIT_TIME = 5#[sec]

def detect_name_posi():
    pag.moveTo(1, 1)
    for count in range(50):
        try:
            x, y, w, h = pag.locateOnScreen('simei.png')
            break
        except ImageNotFoundException:
            time.sleep(1)
    return x, y, w, h

def get_name_img(x, y, w, h, NAME_W):
    start_x = x + w
    start_y = y
    name_img = pag.screenshot(region=(start_x, start_y, NAME_W, h))
    return name_img

def run_ocr(tool, name_img):
    result = tool.image_to_string(name_img, lang='jpn')
    result = result.replace(' ', '')
    print(result)
    return result

def copy_name_data(name_list):
    pag.moveTo(923, 306)
    pag.click()

    for name in name_list:
        pyperclip.copy(name)
        pag.hotkey('ctrl', 'v')
        pag.press('enter')
        pag.press('enter')

if __name__ == '__main__':
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    tool = tools[0]

    name_list = []

    for idx, file in enumerate(todokede_list):
        if idx != 0:
            start = time.time()
            elapsed_time = 0
            while pdf_pro.poll() == None:
                elapsed_time = time.time() - start
                if elapsed_time > WAIT_TIME:
                    print('STOP PROCESS')
                    sys.exit(1)

        print('open :', file)
        pdf_pro = subprocess.Popen([acr_path, todokede_path+file])
        time.sleep(1)

        x, y, w, h = detect_name_posi()

        name_img = get_name_img(x, y, w, h, NAME_W)

        result = run_ocr(tool, name_img)
        name_list.append(result)

        pag.click(CLOSE_BUTTON_X, CLOSE_BUTTON_Y)

    copy_name_data(name_list)

    pag.alert('終了しました')
