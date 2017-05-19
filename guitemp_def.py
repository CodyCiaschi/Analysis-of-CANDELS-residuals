#*- coding: utf-8 -*-
"""
Created on Tue Feb  7 05:15:30 2017

@author: cody
"""

import tkinter
from PIL import Image, ImageTk
import os
import glob

image_list = []

for filename in glob.glob('*.png'):
    image_list.append(filename)

def good_image(good,window):
    good.save("goodtest.png")
    window.destroy()

def bad_image(bad,window):
    bad.save("badtest.png")  
    window.destroy()

def rate_images(testimage):
    top = tkinter.Tk()
    image = Image.open(testimage)
    photo = ImageTk.PhotoImage(image)
    label = tkinter.Label(image=photo)
    label.testimage = photo # keep a reference!
    label.pack()
    
    Button1 = tkinter.Button(top, text="Good",command =  lambda : good_image(image,top))

    Button2 = tkinter.Button(top, text="Bad", command = lambda : bad_image(image,top))
   
    label.pack()
    Button1.pack()
    Button2.pack()
    top.mainloop()


print(image_list)

for i in image_list:
    rate_images(i)
