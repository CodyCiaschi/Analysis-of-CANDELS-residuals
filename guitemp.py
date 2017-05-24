#-*- coding: utf-8 -*-
"""
Created on Tue Feb  7 05:15:30 2017

@author: cody
"""
import csv
import tkinter
from PIL import Image, ImageTk
import glob

def Next(window):
    window.destroy()

def Back(window):
    window.destroy()

def goodImage(number, name):
        with open('testing.csv','a',newline='') as csvfile:
            galwrite = csv.writer(csvfile, delimiter=' ')
            galwrite.writerow([number, name, 'Good'])

def badImage(number, name):
        with open('testing.csv','a',newline='') as csvfile:
            galwrite = csv.writer(csvfile, delimiter=' ')
            galwrite.writerow([number, name, 'Bad'])

def rate_images(ii, filename, testimage):
    top = tkinter.Tk()
    image = Image.open(testimage)
    photo = ImageTk.PhotoImage(image)
    label = tkinter.Label(image=photo)
    label.testimage = photo # keep a reference!
    label.pack()
    
    Button1 = tkinter.Button(top, text="Good",command = lambda: goodImage(ii,testimage))
    Button2 = tkinter.Button(top, text="Bad", command = lambda: badImage(ii,testimage))
    Button3 = tkinter.Button(top, text="Next", command = lambda:  Next(top))
    Button4 = tkinter.Button(top, text="Back", command = lambda: Back(top))

    label.pack()
    Button1.pack()
    Button2.pack()
    Button3.pack()
    Button4.pack()
    top.mainloop()

#will work for png files only but can work for many other image formats eventually
image_list = []
for filename in glob.glob('*.png'):
    image_list.append(filename)

#make csv file with header(other columns can be added)
with open('testing.csv','w',newline='') as csvfile:
    galwrite = csv.writer(csvfile, delimiter=' ')
    galwrite.writerow(['Number', 'Name', 'Quality'])

#now to run all of the images through rate_images
#will use iterator to be able to go back and forth(hopefully)
i=0
while(i < len(image_list)):
    rate_images(i, galwrite, image_list[i])
    i+=1

#make sure this is working
