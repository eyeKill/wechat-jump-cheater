#!/usr/bin/env python3
from cv2 import cv2
from chess import *

img = cv2.imread("rc1.png")
img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(img, 50, 100)
cv2.imwrite("edges.png", edges)