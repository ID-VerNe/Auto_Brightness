# -*- coding: utf-8 -*-
# @Time ： 2021/5/6 11:25
# @E-mail：yuu_seeing@foxmail.com
# @Auth ： VerNe
# @File ： 自动亮度.py
# @IDE ：  PyCharm
import math
import wmi
import cv2
import time
from PIL import ImageStat
from PIL import Image

add = float(input('输入亮度附加值：'))
cap = cv2.VideoCapture(0)
c = wmi.WMI(namespace='root\WMI')

a = c.WmiMonitorBrightnessMethods()[0]

while (1):
    ret, frame = cap.read()  # 读取每一帧
    cv2.imwrite(r'brightness.png', frame)
    im = Image.open(r'brightness.png')
    star = ImageStat.Stat(im)
    rms = star.rms[0]  # 计算均方根灰度
    if rms > 240:
        rms = 240
    elif rms < 32:
        rms = 32
    brightness = 49.63 * math.log(rms) - 172.01 + add
    if brightness <= 10:
        brightness = 10
    print(brightness)
    a.WmiSetBrightness(Brightness=brightness, Timeout=500)
    time.sleep(1)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    last = brightness
