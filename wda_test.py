#!/usr/bin/env python3
import wda
import time
from PIL import Image, ImageFilter, ImageEnhance
from io import BytesIO
import numpy as np

def filter_image(img):
    out1 = img.filter(ImageFilter.GaussianBlur(radius=1))
    out2 = ImageEnhance.Contrast(out1).enhance(2)
    out3 = out2.filter(ImageFilter.FIND_EDGES)#.filter(ImageFilter.SMOOTH_MORE)
    return out3

c = wda.Client('http://localhost:8100')
print(c.status())

with c.session('com.tencent.xin') as s:
    # enter wechat-jump
    # slide down to open app list
    s.swipe(100,100,100,800,0.5)
    # tap on wechat-jump to enter it
    s.tap(50,200)
    # wait for it to load
    time.sleep(2)
    # tap begin
    s.tap(300,1000)
    # here we go
    time.sleep(1.5)
    while(True):
        img = filter_image(Image.open(BytesIO(c.screenshot())))
        img.show()
        t = float(input())
        s.tap_hold(300,500,t)
        time.sleep(1)

