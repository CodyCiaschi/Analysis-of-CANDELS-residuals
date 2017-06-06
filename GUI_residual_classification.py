from Tkinter import *
from PIL import ImageTk, Image
from collections import defaultdict
import numpy as np
import os
from time import gmtime, strftime
import glob
from astropy.io import fits
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import sys


def emulate_image(filepath, gal_id):

    class App:

        def __init__(self, master):

            original  = list(fits.getdata(filepath, 1))
            model = list(fits.getdata(filepath, 2))
            residual = list(fits.getdata(filepath, 3))

            fig = Figure(figsize=(10,10), dpi=100)
            original_plot = fig.add_subplot(131)
            original_plot.imshow(original)

            model_plot = fig.add_subplot(132)
            model_plot.imshow(model)

            residual_plot = fig.add_subplot(133)
            residual_plot.imshow(residual)

            fig.tight_layout()

            frame = Frame(master)
            frame.pack(side = TOP)

            frame2 = Frame(master)
            frame2.pack(side = BOTTOM)

            self.decision = defaultdict(list)

            self.good_residual_button = Checkbutton(frame, text = "Good\n Residual", wraplength = 90, command = self.good_residual)
            self.good_residual_button.pack(side=LEFT)

            self.bad_residual_artifact_button = Checkbutton(frame, text = "Bad\n Residual\n Artifact", wraplength = 90, command = self.bad_residual_artifact)
            self.bad_residual_artifact_button.pack(side = LEFT)

            self.bad_residual_natural_button = Checkbutton(frame, text = "Bad\n Residual\n Natural", wraplength = 90, command = self.bad_residual_natural)
            self.bad_residual_natural_button.pack(side = LEFT)

            self.reasonable_contains_clumps_button = Checkbutton(frame, text = "Reasonable\n Contains\n Clumps",wraplength=90, command=self.reasonable_contains_clumps)
            self.reasonable_contains_clumps_button.pack(side = LEFT)

            self.reasonable_contains_substructure_button = Checkbutton(frame, text = "Reasonable\n Contains\n Substructure", wraplength = 90, command = self.reasonable_contains_substructure)
            self.reasonable_contains_substructure_button.pack(side = LEFT)

            self.tidal_features_present_button = Checkbutton(frame, text = "Tidal\n Features Present", wraplength = 90, command = self.tidal_feature_pres)
            self.tidal_features_present_button.pack(side = LEFT)

            self.tidal_features_not_present_button = Checkbutton(frame, text = "Tidal Features\n Not Present", wraplength = 90, command = self.tidal_feature_not_pres)
            self.tidal_features_not_present_button.pack(side = LEFT)

            self.Done_button = Button(frame, text = "Done !",wraplength = 55, command = self.done)
            self.Done_button.pack(side = LEFT)

            self.canvas = FigureCanvasTkAgg(fig, master = frame2)
            self.canvas.get_tk_widget().pack()

        def good_residual(self):
            if 'GR' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('GR')
            elif 'GR' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('GR')

        def bad_residual_artifact(self):
            if 'BRA' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('BRA')
            elif 'BRA' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('BRA')

        def bad_residual_natural(self):
            if 'BRN' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('BRN')
            elif 'BRN' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('BRN')

        def reasonable_contains_clumps(self):
            if 'RCC' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('RCC')
            elif 'RCC' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('RCC')

        def reasonable_contains_substructure(self):
            if 'RCS' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('RCS')
            elif 'RCS' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('RCS')

        def tidal_feature_pres(self):
            if 'TFP' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('TFP')
            elif 'TFP' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('TFP')

        def tidal_feature_not_pres(self):
            if 'TFNP' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('TFNP')
            elif 'TFNP' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('TFNP')

        def done(self):
            if self.decision['%s'%gal_id] != []:
                root.destroy()
            if self.decision['%s'%gal_id] == []:
                self.decision['%s'%gal_id].append('OK')
                root.destroy()

    root = Tk()
    app = App(root)
    root.resizable(width=True, height = False)
    root.geometry("{}x{}".format(1024,400))
    root.title("Original Image and Residual")
    root.mainloop()

    return(app.decision)

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


if len(sys.argv) == 1:
    path = os.getcwd()
elif len(sys.argv) == 2:
    path = sys.argv[1]

sample = glob.glob(path + '/*.fits')

ids = []
for filenames in sample:
    _, tail = os.path.split(filenames)
    ids.append(tail)

new_decision_dict = dict()

for each in sample:
    _,id = os.path.split(each)
    this_decision = emulate_image(each, id)
    for galaxy,flags in this_decision.items():
        flag_string = str()
        for each in flags:
            flag_string = flag_string+each+'/'
        new_decision_dict[galaxy] = flag_string

final_information_array = [['ID','Visual_check_flag']]

for key,value in new_decision_dict.items():
    final_information_array.append([key,value])
writeCsvFile(os.getcwd()+'/classification_results_%s.csv'%(strftime("%Y-%m-%d %H:%M:%S", gmtime())),final_information_array)
