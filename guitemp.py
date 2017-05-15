#*- coding: utf-8 -*-
"""
Created on Tue Feb  7 05:15:30 2017

@author: cody
"""

import tkinter
from PIL import Image, ImageTk

def good_image(good):
    good.save("goodtest.png")

def bad_image(bad):
    bad.save("badtest.png")  

def rate_images(testimage):
    top = tkinter.Tk()
    image = Image.open(testimage)
    photo = ImageTk.PhotoImage(image)

    label = tkinter.Label(image=photo)
    label.image = photo # keep a reference!
    label.pack()
    
    Button1 = tkinter.Button(top, text="Good",command = lambda : good_image(image) & top.destroy())

    Button2 = tkinter.Button(top, text="Bad", command = lambda : bad_image(image) & top.destroy())
   
    label.pack()
    Button1.pack()
    Button2.pack()
    top.mainloop()

x = ["cms_plot.png","cdms_plot.png"]

for i in x:
    rate_images(i)
