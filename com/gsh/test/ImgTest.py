'''
Created on 2017年11月15日

@author: gdd
'''
from PIL import Image, ImageFont, ImageDraw

import random

msgNum = str((random.randint(1, 99))) #生成随机数

im = Image.open('/Volumes/GSH/Python/gsh.jpg')  #载入图片
w, h = im.size                      #获取图片宽度和高度
wdraw = 0.8*w                   #定义数字坐标
hdraw = 0.05*h
im.save('/Volumes/GSH/Python/gsh.png','png')
im.show()
'''
fron = ImageFont.truetype('xiaoxiangzi.ttf', 30) #载入数值的字体及大小
draw = ImageDraw.Draw(im)  #创建图像
draw.text((wdraw, hdraw), msgNum, font=fron, fill=(255, 33, 33))
'''
#定义图像格式
    #(wdraw, hdraw)：坐标
    #msgNum: 随机数
    # font: 自定义字体及大小
    # fill：定义颜色，可以为数字格式也可以直接指定英文如：fill="red"

im.save('test2.png', 'png')#指定格式保存生成图像即可，
