#!/usr/bin/env python3
import cv2
import numpy as np

fin = open("test.png",mode='rb')
np.asarray(bytearray(fin.read()),dtype=np.uint8)