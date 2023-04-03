import Quartz
from PIL import ImageGrab, Image
import time

import cv2 as cv
import numpy as np
import pyautogui
from mss import mss
import numpy
import pytesseract


def find_object(screen, template, threshold=0.9, debug=False):
    result = cv.matchTemplate(screen, template, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    if debug == True:
        print(max_val)
    if max_val > threshold:
        h, w, _ = template.shape
        top_left = max_loc
        bottom_right = (max_loc[0] + w, max_loc[1] + h)
        cv.rectangle(screen, top_left, bottom_right, (255, 0, 0), 2)
        screen = cv.cvtColor(screen, cv.COLOR_HSV2BGR)
        cv.imshow('CAPTURE', screen)
        x, y = max_loc[0] + w // 2, 95 + max_loc[1] + h // 2
        # pyautogui.click(x / 2, y / 2)
        print('\nat ', x / 2, y / 2)
        print('With score of ', max_val, ' found:')
        return x, y


x, y, width, height = 0, 50, 770, 550
region = (x, y, width, height)


def capture_screenshot(pos=region):
    # Capture entire screen
    with mss() as sct:
        sct_img = sct.grab(pos)
        # Convert to PIL/Pillow Image
        return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')


def new_screenshot():
    screenshot = capture_screenshot()
    screenshot = numpy.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2HSV)

    return screenshot


def get_player_position():
    xhome = 256
    yhome = 226

    pyautogui.moveTo(xhome, yhome)
    time.sleep(0.4)

    left = 249
    top = 246
    width = 90
    height = 35
    bbox = (left, top, left + width, top + height)

    x, y = None, None

    for i in range(100000):
        pyautogui.moveTo(xhome, yhome)
        area = ImageGrab.grab(bbox)

        area = numpy.array(area)
        gray = cv.cvtColor(area, cv.COLOR_BGR2GRAY)
        gray = cv.threshold(gray, 0, 255, cv.THRESH_BINARY | cv.THRESH_OTSU)[1]

        text = pytesseract.image_to_string(gray)
        text = text.replace('.', ' ')
        text = text.replace(',', ' ')

        coords = text.split(' ')

        print(text)

        for i in coords:
            if i == '':
                coords.remove(i)

        try:
            x, y = int(coords[0]), int(coords[1])
            print(x, y)
            return x, y
        except:
            time.sleep(2)
            pyautogui.click(xhome + 30, yhome)
            continue
    exit('player_pos not found')


def go_to_bank():
    inFarm = False
    xhome = 256
    yhome = 226

    gatepos = (3032, 3312)
    pyautogui.moveTo(1000, 1000)
    screenshot = new_screenshot()

    bank = cv.imread('bank.png')
    bank = cv.cvtColor(bank, cv.COLOR_RGB2HSV)

    cowTemplate = cv.imread('start.png')
    cowTemplate = cv.cvtColor(cowTemplate, cv.COLOR_RGB2HSV)

    bigGate = cv.imread('exit.png')
    bigGate = cv.cvtColor(bigGate, cv.COLOR_RGB2HSV)

    entry = cv.imread('entry.png')
    entry = cv.cvtColor(entry, cv.COLOR_RGB2HSV)

    def goto(location=gatepos):
        playerpos = get_player_position()

        x = location[0] - playerpos[0]
        y = location[1] - playerpos[1]

        print(x, y)

        multiplier = 1
        if x < 0:
            multiplier = -1

        while abs(x) > 0:
            if x >= 8:
                x -= (8 * multiplier)
                xmove = 8 * 26 * multiplier + xhome
                xtime = 0.95 * 8
            else:
                xtime = abs(x) * 0.95
                xmove = x * 26 + xhome
                x -= x
            pyautogui.click(xmove, yhome)
            time.sleep(xtime)

        multiplier = -1
        if y < 0:
            multiplier = 1

        while abs(y) > 0:
            if y >= 5:
                y -= (5 * -multiplier)
                ymove = 5 * 26 * multiplier + yhome
                ytime = 0.95 * 5
            else:
                ytime = abs(y) * 0.95
                ymove = abs(y) * 20 * multiplier + yhome
                y -= y
            pyautogui.click(xhome, ymove)
            time.sleep(ytime)

    screenshot = new_screenshot()

    object = find_object(screenshot, bigGate, 0.7, True)

    cow = find_object(screenshot, cowTemplate, 0.7, True)

    playerpos = get_player_position()

    while not object or playerpos != gatepos or cow:
        if cow:
            print('god fucking damn it.....')
            time.sleep(20)

        goto()

        screenshot = new_screenshot()
        object = find_object(screenshot, bigGate, 0.75)
        playerpos = get_player_position()
        cow = find_object(screenshot, cowTemplate, 0.7)

    while object or cow or playerpos[0] != 3032:
        if cow:
            print('god fucking damn it.....')
            time.sleep(10)
        screenshot = new_screenshot()
        object = find_object(screenshot, bigGate, 0.75)
        time.sleep(2)
        if object:
            pyautogui.click(object[0] / 2, object[1] / 2 + 12)
        time.sleep(2)
        playerpos = get_player_position()
        if playerpos[0] != 3032:
            pyautogui.click(xhome + 26, yhome + 60)
            time.sleep(3)
            goto()
            time.sleep(2)
            playerpos = get_player_position()
        cow = find_object(screenshot, cowTemplate, 0.7)

    pyautogui.click(581, 112)
    time.sleep(15)
    pyautogui.click(603, 87)
    time.sleep(15)
    pyautogui.click(645, 70)
    time.sleep(13)
    pyautogui.click(660, 110)
    time.sleep(15)

    screenshot = new_screenshot()
    time.sleep(0.5)
    object = find_object(screenshot, bank, 0.7, True)
    time.sleep(0.5)
    pyautogui.click(object[0] / 2, object[1] / 2)
    time.sleep(0.2)
    pyautogui.click(object[0] / 2, object[1] / 2)
    time.sleep(0.5)
    pyautogui.click(579, 283)
    time.sleep(1)
    pyautogui.click(618, 283)
    time.sleep(1)
    pyautogui.click(661, 283)
    time.sleep(1)
    pyautogui.click(702, 283)
    time.sleep(1)
    pyautogui.click(407, 77)
    time.sleep(1)

    pyautogui.click(622, 189)
    time.sleep(15)
    pyautogui.click(644, 200)
    time.sleep(14)
    pyautogui.click(700, 166)
    time.sleep(14)
    pyautogui.click(676, 159)
    time.sleep(10)
    pyautogui.click(643, 176)
    time.sleep(7)


# COW BUSINESS
cowDia = cv.imread('cow.png')
# cowHorT = cv.imread('cowHorT.png')
cowHor = cv.imread('cowHor.png')
cowVer = cv.imread('cowVer.png')
drop = cv.imread('drop.png')
start = cv.imread('start.png')
dead = cv.imread('dead.png')
full = cv.imread('FULL.png')

cowDia = cv.cvtColor(cowDia, cv.COLOR_RGB2HSV)
# cowHorT = cv.cvtColor(cowHorT, cv.COLOR_RGB2HSV)
cowHor = cv.cvtColor(cowHor, cv.COLOR_RGB2HSV)
dropVer = cv.cvtColor(cowVer, cv.COLOR_RGB2HSV)
drop = cv.cvtColor(drop, cv.COLOR_RGB2HSV)
start = cv.cvtColor(start, cv.COLOR_RGB2HSV)
dead = cv.cvtColor(dead, cv.COLOR_RGB2HSV)
full = cv.cvtColor(full, cv.COLOR_RGB2HSV)

items = [(drop, 0.7), (cowDia, 0.5), (cowHor, 0.5), (cowVer, 0.5)]  # (cowHorT, 0.5)]

xhome = 256
yhome = 226

while True:

    for i in items:
        screenshot = new_screenshot()
        demo = cv.cvtColor(screenshot, cv.COLOR_HSV2BGR)
        cv.imshow('CAPTURE', demo)

        object = find_object(screenshot, i[0], threshold=i[1])

        if cv.waitKey(1) == ord('q'):
            cv.destroyAllWindows()
            exit('DONE')
        if object is not None:
            if i[1] > 0.65:
                pyautogui.click(object[0] / 2, object[1] / 2)
                print('DROP.')
                time.sleep(5)
                screenshot = new_screenshot()
                demo = cv.cvtColor(screenshot, cv.COLOR_HSV2BGR)
                cv.imshow('CAPTURE', demo)
                if find_object(screenshot, full, 0.7, True):
                    go_to_bank()
                break
            else:
                print('A COW!')
                x = object[0]
                y = object[1]
                pyautogui.click(x / 2, y / 2)
                time.sleep(4)
                screenshot = new_screenshot()
                demo = cv.cvtColor(screenshot, cv.COLOR_HSV2BGR)
                cv.imshow('CAPTURE', demo)
                if find_object(screenshot, start, 0.7) == None:
                    print('Cow missed')
                else:
                    print('Cow hit!')
                    while find_object(screenshot, dead, 0.8) == None:
                        time.sleep(1)
                        print("Killing cow...")
                        screenshot = new_screenshot()
                        demo = cv.cvtColor(screenshot, cv.COLOR_HSV2BGR)
                        cv.imshow('CAPTURE', demo)
                    print("\nCow Dead!")
                break
