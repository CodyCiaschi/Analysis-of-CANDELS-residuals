from Tkinter import *
from collections import defaultdict
import numpy as np
import os
from time import gmtime, strftime
import glob
from astropy.io import fits
import matplotlib

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.colors import SymLogNorm
import sys
import remove_outliers as ro
import tkMessageBox

def create_image(filepath):
    cube = fits.open(filepath, memmap=True)

    original = cube[1].data
    model = cube[2].data
    residual = cube[3].data

    original_clipped = ro.removeoutliers(np.array(original.flat), nsigma=7, remove='both', center='median',
                                         niter=np.Inf, retind=False, verbose=False)

    model_clipped = ro.removeoutliers(np.array(original.flat), nsigma=7, remove='both', center='median',
                                      niter=np.Inf, retind=False, verbose=False)

    residual_clipped = ro.removeoutliers(np.array(original.flat), nsigma=7, remove='both', center='median',
                                         niter=np.Inf, retind=False, verbose=False)

    fig = Figure(figsize=(30, 30), dpi=100)

    original_plot = fig.add_subplot(131)
    original_plot.imshow(original, cmap='gray', origin='lower',
                         norm=SymLogNorm(.009, linscale=.5, vmin=np.min(original_clipped), vmax=np.max(original)*5))
    fig.gca().set_axis_off()

    model_plot = fig.add_subplot(132)
    model_plot.imshow(model, cmap='gray', origin='lower',
                      norm=SymLogNorm(0.009, linscale=.5, vmin=min(model_clipped), vmax=np.max(model_clipped) * 5))
    fig.gca().set_axis_off()

    residual_plot = fig.add_subplot(133)
    residual_plot.imshow(residual, cmap='gray', origin='lower',
                         norm=SymLogNorm(0.009, linscale=0.5, vmin=min(residual_clipped),
                                         vmax=np.max(residual_clipped) * 5))
    fig.gca().set_axis_off()

    return fig


def emulate_image(filepath, gal_id):
    root = Tk()

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()

    x = (sw / 4)
    y = (sh / 4)

    app = App(root, filepath, gal_id)
    root.resizable(width=True, height=False)
    root.geometry("{}x{}+{}+{}".format(1024, 400, x, y))
    root.title("Original Image and Residual")
    root.mainloop()

    return app.decision


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


class App:
    def __init__(self, master, filepath, gal_id):

        master_frame = Frame(master)
        master_frame.pack(side=TOP)

        clean_residuals = LabelFrame(master_frame, text='Clean Residual')
        clean_residuals.pack(side=LEFT, padx=10)

        core_residuals = LabelFrame(master_frame, text='Core Residuals')
        core_residuals.pack(side=LEFT)

        natural_residuals = LabelFrame(master_frame, text='Natural Residuals')
        natural_residuals.pack(side = LEFT,padx = 10)

        tidal_features = LabelFrame(master_frame, text='Tidal Features')
        tidal_features.pack(side=LEFT)

        image = Frame(master)
        image.pack(side=BOTTOM)

        fig = create_image(filepath)

        self.decision = defaultdict(list)

        self.gal_id = gal_id
        self.filepath = filepath
        self.root = master

        self.good_residual_button = Checkbutton(clean_residuals, text="Clean\n Residual", wraplength=90,
                                                command=self.clean_residual)
        self.good_residual_button.grid(row=0,column=0)

        self.good_residual_button = Checkbutton(core_residuals, text="Over/Under", wraplength=90,
                                                command=self.over_under)
        self.good_residual_button.grid(row=0, column=0)

        self.good_residual_button = Checkbutton(core_residuals, text="Under/Over", wraplength=90,
                                                command=self.under_over)
        self.good_residual_button.grid(row=0, column=1)

        self.striated_button = Checkbutton(core_residuals, text='Striated', wraplength=90, command=self.striated)
        self.striated_button.grid(row=1, column=0)

        self.residual_artifact_button = Checkbutton(core_residuals, text="Residual\n Artifact", wraplength=90,
                                                        command=self.residual_artifact)
        self.residual_artifact_button.grid(row=1, column=1)

        self.unfit_disk_button = Checkbutton(natural_residuals, text="Unfit\n Disk", wraplength=90,
                                                       command=self.unfit_disk)
        self.unfit_disk_button.grid(row=0, column=0)

        self.unfit_spiral_arms_button = Checkbutton(natural_residuals, text="Unfit\n Spiral Arms", wraplength=90,
                                             command=self.unfit_sprial_arms)
        self.unfit_spiral_arms_button.grid(row=0, column=1)

        self.contains_substructure_button = Checkbutton(natural_residuals, text="Contains\n Substructure",
                                                                   wraplength=90,
                                                                   command=self.contains_substructure)
        self.contains_substructure_button.grid(row=1, column=0)

        self.asymmetric_fit_button = Checkbutton(natural_residuals, text="Asymmetric\n Fit",
                                                        wraplength=90,
                                                        command=self.asymmetric_fit)
        self.asymmetric_fit_button.grid(row=1, column=1)

        self.tidal_features_present_button = Checkbutton(tidal_features, text="Tidal\n Features Present", wraplength=90,
                                                         command=self.tidal_feature_pres)
        self.tidal_features_present_button.grid(row=0,column=0)

        self.tidal_features_possible_button = Checkbutton(tidal_features, text="Tidal\n Features Possible", wraplength=90,
                                                         command=self.tidal_feature_poss)
        self.tidal_features_possible_button.grid(row=0, column=1)

        self.Done_button = Button(master_frame, text="Done !", wraplength=55, command=self.done)
        self.Done_button.pack(side=RIGHT, anchor=E, padx = 10)

        self.canvas = FigureCanvasTkAgg(fig, master=master)
        self.canvas.get_tk_widget().pack()

    def clean_residual(self):
        if 'CR' not in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].append('CR')
        elif 'CR' in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].remove('CR')

    def residual_artifact(self):
        if 'RA' not in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].append('RA')
        elif 'RA' in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].remove('RA')

    def over_under(self):
        if 'OU' not in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].append('OU')
        elif 'OU' in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].remove('OU')

    def under_over(self):
        if 'UO' not in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].append('UO')
        elif 'UO' in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].remove('UO')

    def striated(self):
        if 'STR' not in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].append('STR')
        elif 'STR' in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].remove('STR')

    def unfit_disk(self):
        if 'UD' not in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].append('UD')
        elif 'UD' in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].remove('UD')

    def unfit_sprial_arms(self):
        if 'USA' not in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].append('USA')
        elif 'USA' in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].remove('USA')

    def contains_substructure(self):
        if 'RCS' not in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].append('RCS')
        elif 'RCS' in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].remove('RCS')

    def asymmetric_fit(self):
        if 'AF' not in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].append('AF')
        elif 'AF' in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].remove('AF')

    def tidal_feature_pres(self):
        if 'TFP' not in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].append('TFP')
        elif 'TFP' in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].remove('TFP')

    def tidal_feature_poss(self):
        if 'TPOSS' not in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].append('TPOSS')
        elif 'TPOSS' in self.decision['%s' % self.gal_id]:
            self.decision['%s' % self.gal_id].remove('TPOSS')

    def done(self):
        if self.decision['%s' % self.gal_id] != []:
            self.root.destroy()
        if self.decision['%s' % self.gal_id] == []:
            tkMessageBox.showwarning('Error', 'No options were chosen. Please choose an option and try again!')
            self.root.mainloop()


# allow the user to call any folder they want
if len(sys.argv) == 1:
    path = os.getcwd()
elif len(sys.argv) == 2:
    path = sys.argv[1]

sample = glob.glob(path + '/*.fits')

new_decision_dict = dict()

for each in sample:
    _, id = os.path.split(each)
    this_decision = emulate_image(each, id)
    for galaxy, flags in this_decision.items():
        flag_string = str()
        for each in flags:
            flag_string = flag_string + each + '/'
        new_decision_dict[galaxy] = flag_string

final_information_array = [['ID', 'Visual_check_flag']]

for key, value in new_decision_dict.items():
    final_information_array.append([key, value])
writeCsvFile(os.getcwd() + '/classification_results_%s.csv' % (strftime("%Y-%m-%d %H:%M:%S", gmtime())),
             final_information_array)
