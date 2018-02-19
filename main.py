#!/usr/bin/env python3
import time
import wda
from cv2 import cv2
import numpy as np

# configurations
DEVICE_URL = "http://localhost:8100"
CHESS_ANCHOR_X_RATIO = 0.5
CHESS_ANCHOR_Y_RATIO = 0.9

# preparations
# load template
chess = cv2.imread("chess.png")
chess_anchor_x = int(CHESS_ANCHOR_X_RATIO * len(chess[0]))
chess_anchor_y = int(CHESS_ANCHOR_Y_RATIO * len(chess))
# load wda Client
c = wda.Client(DEVICE_URL)
print(c.status())
case_no = 0

def find_chess(img):
    res = cv2.matchTemplate(img, chess, cv2.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    return max_loc[0] + chess_anchor_x, max_loc[1] + chess_anchor_y

def find_dest(img, chess_anchor):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.Canny(img, 20, 70)
    if chess_anchor[0] < 375:
        y_top = np.nonzero(img[400:chess_anchor[1], 390:])[0][0] + 400
        x_top = int(np.mean(np.nonzero(img[y_top])))
    else:
        y_top = np.nonzero(img[400:chess_anchor[1], :360])[0][0] + 400
        x_top = int(np.mean(np.nonzero(img[y_top])))
    cv2.line(img, (0, y_top), (1000, y_top), 200)
    cv2.line(img, (x_top, 0), (x_top, 2000), 200)
    x_anchor = x_top
    y_anchor = int(chess_anchor[1] -
                   np.abs(x_anchor - chess_anchor[0]) / np.sqrt(3))
    cv2.line(img, chess_anchor, (x_anchor, y_anchor), 255)
    cv2.circle(img, (x_anchor, y_anchor), 5, 255, 5)
    cv2.imwrite(f"case{case_no}_edges.png", img)
    return x_anchor, y_anchor

with c.session('com.tencent.xin') as s:
    # enter wechat-jump
    # slide down to open app list
    s.swipe(100, 200, 100, 1200, 0.5)
    # tap on wechat-jump to enter it
    s.tap(50, 200)
    # wait for it to load
    time.sleep(2)
    # tap begin
    s.tap(300, 1000)
    time.sleep(1)
    # here we go
    while(True):
        img_array = np.asarray(bytearray(c.screenshot()), dtype=np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        if np.mean(img[:450, :250]) < 50:
            # game over
            break

        chess_anchor = find_chess(img)
        print(chess_anchor, '-', end='', sep='')
        dest_anchor = find_dest(img, chess_anchor)
        length = np.linalg.norm(np.array(chess_anchor) - np.array(dest_anchor))
        print(dest_anchor, 'length=', length, sep='')
        cv2.circle(img, chess_anchor, 5, (255, 0, 0), 5)
        cv2.circle(img, dest_anchor, 5, (0, 0, 255), 5)
        case_no += 1
        cv2.waitKey(1)
        s.tap_hold(int(np.random.random() * 100) + 300,
                   int(np.random.random() * 100) + 600, length * 0.002)
        time.sleep(1.25)

cv2.destroyAllWindows()
