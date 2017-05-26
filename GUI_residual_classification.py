from Tkinter import *
from PIL import ImageTk, Image
from collections import defaultdict
import numpy as np
import os
from time import gmtime, strftime
def emulate_image(file_path, gal_id):

    class App:

        def __init__(self, master):

            frame = Frame(master)
            frame.pack()
            self.decision = defaultdict(list)

            self.good_residual_button = Checkbutton(frame, text="Good\n Residual",wraplength=75, command=self.good_residual)
            self.good_residual_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)

            self.bad_residual_button = Checkbutton(frame, text="Bad\n Residual",wraplength=55, command=self.bad_residual)
            self.bad_residual_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)

            self.interacting_button = Checkbutton(frame, text="\n Interacting",wraplength=75, command=self.interacting)
            self.interacting_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)

            self.possibly_interacting_button = Checkbutton(frame, text="Possibly\n Interacting",wraplength=75, command=self.possibly_interacting)
            self.possibly_interacting_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)

            self.not_interacting_button = Checkbutton(frame, text="Not\n Interacting",wraplength=75, command=self.not_interacting)
            self.not_interacting_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)

            self.tidal_features_present_button = Checkbutton(frame, text="Tidal\n Features Present",wraplength=75, command=self.tidal_feature_pres)
            self.tidal_features_present_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)

            self.tidal_features_not_present_button = Checkbutton(frame, text="Tidal Features\n Not Present",wraplength=75, command=self.tidal_feature_not_pres)
            self.tidal_features_not_present_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)

            self.Done_button = Button(frame, text="Done !",wraplength=55, command=self.done)
            self.Done_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)

        def good_residual(self):
            if 'GR' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('GR')
            elif 'GR' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('GR')

        def bad_residual(self):
            if 'BR' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('BR')
            elif 'BR' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('BR')

        def interacting(self):
            if 'interacting' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('interacting')
            elif 'interacting' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('interacting')

        def possibly_interacting(self):
            if 'poss_interacting' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('poss_interacting')
            elif 'poss_interacting' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('poss_interacting')

        def not_interacting(self):
            if 'not_interacting' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('not_interacting')
            elif 'not_interacting' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('not_interacting')

        def tidal_feature_pres(self):
            if 'TFP' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('TFP')
            elif 'not_interacting' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('TFP')

        def tidal_feature_not_pres(self):
            if 'TFNP' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('TFNP')
            elif 'not_interacting' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('TFNP')

        def done(self):
            if self.decision['%s'%gal_id] != []:
                root.destroy()
            if self.decision['%s'%gal_id] == []:
                self.decision['%s'%gal_id].append('OK')
                root.destroy()


    root = Tk()
    app = App(root)
    root.geometry("+{}+{}".format(20,50))
    root.title("Original Image and Residual")

    imageFile1 = file_path + 'CMS_ID_' + gal_id + '_kpc.png'
    imageFile2 = file_path + 'CMS_ID_' + gal_id + '_pix.png'

    image1 = Image.open(imageFile1).resize((700, 500))
    image2 = Image.open(imageFile2).resize((700, 500))
    # PIL's ImageTk converts to an image object that Tkinter can handle
    photo1 = ImageTk.PhotoImage(image1)
    photo2 = ImageTk.PhotoImage(image2)

    # put the image objects on labels in a grid layout
    label1 = Label(root,image=photo1)
    label2 = Label(root,image=photo2)


    label1.pack(side=LEFT)
    label2.pack(side=RIGHT)
    root.mainloop()

    return(app.decision)

def scan_current_folder():
    list_of_files=os.listdir(os.getcwd())
    list_of_id=[]
    for each in list_of_files:
        if each.endswith('.png'):
            list_of_id.append(each.split('_')[2])
    return(list_of_id)

def writeCsvFile(fname, data, *args, **kwargs):
    import csv
    """
    @param fname: string, name of file to write
    @param data: list of list of items

    Write data to file
    """
    mycsv = csv.writer(open(fname, 'wb'), *args, **kwargs)
    for row in data:
        mycsv.writerow(row)

random_sample = scan_current_folder()
no_id_duplicates = list(set(random_sample))

new_decision_dict = dict()
for each in no_id_duplicates:
    this_decision = emulate_image(os.getcwd()+'/',each)
    for galaxy,flags in this_decision.items():
        flag_string = str()
        for each in flags:
            flag_string = flag_string+each+'/'
        new_decision_dict[galaxy] = flag_string

final_information_array = [['ID','Visual_check_flag']]
for key,value in new_decision_dict.items():
    final_information_array.append([key,value])
writeCsvFile(os.getcwd()+'/classification_results_%s.csv'%(strftime("%Y-%m-%d %H:%M:%S", gmtime())),final_information_array)
