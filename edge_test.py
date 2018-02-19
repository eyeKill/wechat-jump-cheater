#!/usr/bin/env python3
import cv2
import numpy as np

testcase = cv2.imread("edges.png",0)
chess_anchor = (270, 766)

def get_dest(img, chess_anchor):
    y_top = np.nonzero(img[400:])[0][0] + 400
    x_top = int(np.mean(np.nonzero(img[y_top])))
    x_anchor = x_top
    y_anchor = int(chess_anchor[1] - (x_anchor - chess_anchor[0]) / np.sqrt(3))
    cv2.circle(img,chess_anchor,5,255,5)
    cv2.circle(img,(x_anchor, y_anchor),5,255,5)
    return (x_anchor, y_anchor)

if __name__ == '__main__':
    get_dest(testcase,chess_anchor)