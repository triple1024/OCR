import pyautogui as pag
import pyocr
from PIL import Image
import sys
import subprocess

import pyperclip
import os
import time

from pyautogui import ImageNotFoundException


# print("マウスカーソルの位置を確認します。5秒以内にクリックしたい位置にカーソルを移動してください。")
# time.sleep(5)

# 現在のマウスカーソルの位置を取得
# x, y = pag.position()
# print(f"現在のマウスカーソルの位置: x={x}, y={y}")

C_btn_x = 336
C_btn_y = 74

acr_path = '/Applications/Adobe Acrobat Reader.app/Contents/MacOS/AdobeReader'
td_path = "/Users/itschoolkanazawawest/OCR/todokede_data/"

td_list = sorted(os.listdir(td_path))

NAME_W = 110
WAIT_TIME = 5

def name_position():
    pag.moveTo(1, 1)
    for count in range(50):
        try:
            x, y, w, h = pag.locateOnScreen('/Users/itschoolkanazawawest/OCR/name.png')
            # macの場合は1/2
            x, y, w, h = x // 2, y // 2, w // 2, h // 2
            break
        except ImageNotFoundException:
            time.sleep(5)
    return x, y, w, h

# def temp(x, w):
#         end_x = 1075
#         start_x = (x + w) // 2
#         NAME_W = end_x - start_x
#         print( NAME_W )


def get_name_img(x, y, w, h, NAME_W):
    start_x = x + w
    start_y = y
    try:
        print(f"Taking screenshot with region: start_x={start_x}, start_y={start_y}, width={NAME_W}, height={h}")
        name_img = pag.screenshot( region=(start_x,  start_y, NAME_W, h))
        print("名前の画像を正常に取得しました。")
        # name_img.save('temp.png')
        return name_img
    except Exception as e:
        print("名前の画像を取得中にエラーが発生しました:", e)
        return None

def run_ocr(tool, name_img):
    result = tool.image_to_string(name_img, lang='jpn')
    result = result.replace(' ', '')
    print(result)
    return result

def data_copy(name_list):
    pag.moveTo(1378,363)
    pag.click()

    for name in name_list:
        print(name)
        pyperclip.copy(name)
        pag.hotkey('command', 'v')
        pag.press('return')
        pag.press('return')

if __name__ == '__main__':

    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found")
        sys.exit(1)
    tool = tools[0]

    name_list = []

    for idx, file in enumerate(td_list):
        if idx != 0:
            start = time.time()
            elapsed_time = 0
            while pdf_pro.poll() == None:
                elapsed_time = time.time() - start
                if elapsed_time > WAIT_TIME:
                    print('STOP PROCESS')
                    sys.exit(1)
            # pdf_pro.wait()
            # time.sleep(WAIT_TIME)

        print('open :', file)
        pdf_pro = subprocess.Popen([acr_path, td_path+file])
        time.sleep(5)  # PDFが開くまでの待機時間を十分に取る

        try:
            x, y, w, h =  name_position()
            print(f"Found image at: x={x}, y={y}, width={w}, height={h}")


            name_img = get_name_img(x, y, w, h, NAME_W)
        except ImageNotFoundException as e:
            print(e)
            continue

        result = run_ocr(tool, name_img)
        name_list.append(result)

        pag.click(C_btn_x, C_btn_y)

    data_copy(name_list)

    pag.alert('終了しました')

