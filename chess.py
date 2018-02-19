#!/usr/bin/env python3
import cv2
import time
template = cv2.imread("chess2.png",0)

cw, ch = (61, 154)
cw_anchor = int(cw * 0.5)
ch_anchor = int(ch * 0.91)

def get_chess_anchor(img):
    res = cv2.matchTemplate(img,template,cv2.TM_CCORR_NORMED)
    min_value, max_value, min_loc, max_loc = cv2.minMaxLoc(res)
    return (max_loc[0] + cw_anchor, max_loc[1] + ch_anchor)

if __name__ == '__main__':
    print(get_chess_anchor(cv2.imread("test.png",0)))