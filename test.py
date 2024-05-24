import cv2
import subprocess
import os
import time

C_btn_x = 336
C_btn_y = 74

acr_path = '/Applications/Adobe Acrobat Reader.app/Contents/MacOS/AdobeReader'
td_path = "/Users/itschoolkanazawawest/OCR/todokede_data/"

td_list = sorted(os.listdir(td_path))

def name_position():
    for count in range(50):
        try:
            screenshot = cv2.imread('screenshot.png')
            gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            template = cv2.imread('name.png', 0)
            result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            if max_val > 0.8:  # マッチングの信頼性を調整するための閾値
                h, w = template.shape[:2]
                return max_loc[0], max_loc[1], w, h
        except Exception:
            time.sleep(1)
    raise Exception("Could not locate the image 'name.png' after 50 tries")

def calculate_name_w(x, w):
    end_x = 1075  # ここを適切な値に設定してください
    NAME_W = end_x - (x + w)
    print(f"end_x: {end_x}, start_x: {x + w}, NAME_W: {NAME_W}")
    if NAME_W <= 0:
        raise ValueError(f"Calculated NAME_W is non-positive: {NAME_W}. Check the coordinates.")
    return NAME_W

def get_name_img(x, y, w, h, NAME_W):
    start_x = x + w
    start_y = y
    try:
        screenshot = cv2.imread('screenshot.png')
        name_img = screenshot[start_y:start_y+h, start_x:start_x+NAME_W]
        cv2.imwrite('temp.png', name_img)
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
            x, y, w, h = name_position()
            print(f"Found image at: x={x}, y={y}, width={w}, height={h}")

            # 期待する座標と一致するかチェック
            if (x, y, w, h) != (888, 535, 55, 25):
                print("Recognized coordinates do not match expected coordinates (888, 535, 55, 25).")
                print("Check image file and screen configuration.")
                continue

            NAME_W = calculate_name_w(x, w)
            name_img = get_name_img(x, y, w, h, NAME_W)

            # ボタンをクリック
            pag.click(C_btn_x, C_btn_y)
            time.sleep(1)

            if idx == 0:
                break
        except Exception as e:
            print(e)
