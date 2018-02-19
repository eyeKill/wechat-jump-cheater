#!/usr/bin/env python3
import wda
from io import BytesIO
import cv2

c = wda.Client()
print(c.status())

img = cv2.imdecode()
