#!/usr/bin/env python3
import time
import wda
from cv2 import cv2
import numpy as np

# configurations
DEVICE_URL = "http://localhost:8100"
TOUCH_TIME_RATIO = 0.002

# preparations
# load template
chess = cv2.imread("chess.png")
chess_anchor_x = int(0.5 * len(chess[0]))
chess_anchor_y = int(0.9 * len(chess))
# load wda Client
c = wda.Client(DEVICE_URL)
print(c.status())
case_no = 0

def find_chess(img):
    '''Find the chess on the screen using simple template matching method.'''
    res = cv2.matchTemplate(img, chess, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_loc[0] + chess_anchor_x, max_loc[1] + chess_anchor_y

def find_dest(img, chess_anchor):
    '''Find the destination of the chess on screen.'''
    # edge detection
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.Canny(img, 20, 70)
    # find the highest edge point
    if chess_anchor[0] < 375:
        y_top = np.nonzero(img[400:chess_anchor[1], 400:])[0][0] + 400
        x_top = int(np.mean(np.nonzero(img[y_top])))
    else:
        y_top = np.nonzero(img[400:chess_anchor[1], :350])[0][0] + 400
        x_top = int(np.mean(np.nonzero(img[y_top])))
    cv2.line(img, (0, y_top), (1000, y_top), 200)
    cv2.line(img, (x_top, 0), (x_top, 2000), 200)
    # find the destination point by
    # drawing a k=+/-sqrt(3) line to connect it with the chess anchor
    x_anchor = x_top
    y_anchor = int(chess_anchor[1] -
                   np.abs(x_anchor - chess_anchor[0]) / np.sqrt(3))
    cv2.line(img, chess_anchor, (x_anchor, y_anchor), 255)
    cv2.circle(img, (x_anchor, y_anchor), 5, 255, 5)
    cv2.imwrite(f"case{case_no}_edges.png", img)
    return x_anchor, y_anchor

with c.session('com.tencent.xin') as s:
    print("Opening wechat. Open it manually if your phone has no respond.")
    s.orientation = wda.PORTRAIT
    # enter wechat-jump
    # slide down to open app list
    s.swipe(100, 200, 100, 1200, 0.5)
    # tap on wechat-jump to enter it
    s.tap(50, 200)
    # wait for it to load
    time.sleep(2)
    # tap begin
    s.tap(375, 1100)
    time.sleep(1)
    # here we go
    while(True):
        print(f'case{case_no:4}', end = ' ')
        t = time.time()
        img_array = np.asarray(bytearray(c.screenshot()), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        td = time.time()
        if np.mean(img[:450, :250]) < 50:
            # game over
            break

        chess_anchor = find_chess(img)
        dest_anchor = find_dest(img, chess_anchor)
        length = np.linalg.norm(np.array(chess_anchor) - np.array(dest_anchor))
        ta = time.time()
        print(f'{chess_anchor} - {dest_anchor}', end = ' ')
        print(f'length ={length:6.5}', end=' ')
        print(f'time used:{td-t:5.3}s/{ta-td:5.3}s/{ta-t:5.3}s')
        cv2.circle(img, chess_anchor, 5, (255, 0, 0), 5)
        cv2.circle(img, dest_anchor, 5, (0, 0, 255), 5)
        case_no += 1
        s.tap_hold(int(np.random.random() * 100) + 300,
                   int(np.random.random() * 100) + 600, length * TOUCH_TIME_RATIO)
        time.sleep(1.2)
    print("Game over. Type in anything to exit.")
    input()

cv2.destroyAllWindows()
