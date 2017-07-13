from Tkinter import *
from optparse import OptionParser
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
import tkFont


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

    fig = Figure(figsize=(100, 100), dpi=100)

    original_plot = fig.add_subplot(131)
    original_plot.imshow(original, cmap='gray', origin='lower',
                         norm=SymLogNorm(.009, linscale=.5, vmin=np.min(original_clipped), vmax=np.max(original) * 5))
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
    root.geometry("{}x{}+{}+{}".format(1200, 500, x, y))
    root.title("Original Image and Residual")
    root.mainloop()

    if app.breakout == 0:
        return app.decision
    elif app.breakout == 1:
        return True

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


class Galaxy:
    def __init__(self, ID):
        self.gal_id = ID
        self.clean_residual = 0
        self.bright_center = 0
        self.dark_center = 0
        self.bright_ring = 0
        self.dark_ring = 0
        self.core_other = 0
        self.artifact = 0
        self.disk = 0
        self.global_other = 0
        self.spiral_arms = 0
        self.asymmetric = 0
        self.bar = 0
        self.diffraction_spikes = 0
        self.image_edge = 0
        self.unfit_neighbor = 0
        self.tidal_features_pres = 0
        self.tidal_features_poss = 0

    def makecsvline(self):
        line = '%s, %i, %i, %i, %i, %i, %i, %i, %i, %i, %i, %i, %i, %i, %i, %i, %i, %i\n' % (
            self.gal_id, self.clean_residual, self.bright_center, self.dark_center,
            self.bright_ring, self.dark_ring, self.core_other, self.artifact,
            self.disk, self.global_other, self.spiral_arms, self.asymmetric,
            self.bar, self.diffraction_spikes, self.image_edge, self.unfit_neighbor, self.tidal_features_pres,
            self.tidal_features_poss)
        return line

    def add_all(self):
        added = self.clean_residual + self.bright_center + self.dark_center + self.bright_ring + self.dark_ring + self.core_other + self.artifact + self.disk + self.global_other + self.spiral_arms + self.asymmetric + self.bar + self.diffraction_spikes + self.image_edge + self.unfit_neighbor + self.tidal_features_pres + self.tidal_features_poss
        return added


class App():
    def __init__(self, master, filepath, gal_id):

        master_frame = Frame(master)
        master_frame.pack(side=TOP)

        clean_residuals = LabelFrame(master_frame, text='Clean Residual', font=("Arial", 14, "bold"), labelanchor='n')
        clean_residuals.pack(side=LEFT, padx=10)

        core_residuals = LabelFrame(master_frame, text='Core Residuals', font=("Arial", 14, "bold"), labelanchor='n')
        core_residuals.pack(side=LEFT)

        natural_residuals = LabelFrame(master_frame, text='Global Residuals', font=("Arial", 14, "bold"),
                                       labelanchor='n')
        natural_residuals.pack(side=LEFT, padx=10)

        artifacts = LabelFrame(master_frame, text='Poor-Fit Artifacts', font=("Arial", 14, "bold"),
                               labelanchor='n')
        artifacts.pack(side=LEFT, padx=10)

        tidal_features = LabelFrame(master_frame, text='Tidal Features', font=("Arial", 14, "bold"), labelanchor='n')
        tidal_features.pack(side=LEFT)

        image = Frame(master)
        image.pack()

        save = Frame(master)
        save.pack(side=BOTTOM)

        fig = create_image(filepath)

        self.newgal = Galaxy(gal_id)

        self.gal_id = gal_id
        self.filepath = filepath
        self.root = master
        self.decision = str()
        self.breakout = 0

        # Clean Residual

        self.clean_residual_button = Button(clean_residuals, text="Clean\n Residual", wraplength=90,
                                                command=self.clean_residual, font=("Arial", 14))
        self.clean_residual_button.grid(row=0, column=1)

        # Core Residuals

        self.bright_center_button = Checkbutton(core_residuals, text="Bright Center", wraplength=90,
                                                command=self.bright_center, font=("Arial", 14))
        self.bright_center_button.grid(row=0, column=0)

        self.dark_ring_button = Checkbutton(core_residuals, text="Dark Ring",
                                            wraplength=90,
                                            command=self.dark_ring, font=("Arial", 14))
        self.dark_ring_button.grid(row=0, column=1)

        self.dark_center_button = Checkbutton(core_residuals, text="Dark Center",
                                              wraplength=90,
                                              command=self.dark_center, font=("Arial", 14))
        self.dark_center_button.grid(row=1, column=0)

        self.bright_ring_button = Checkbutton(core_residuals, text="Bright Ring",
                                              wraplength=90,
                                              command=self.bright_ring, font=("Arial", 14))
        self.bright_ring_button.grid(row=1, column=1)

        self.core_other_button = Checkbutton(core_residuals, text='Other', wraplength=90, command=self.core_other,
                                           font=("Arial", 14))
        self.core_other_button.grid(row=0, column=3)

        # Global Residuals

        self.disk_button = Checkbutton(natural_residuals, text=" Disk", wraplength=90,
                                       command=self.disk, font=("Arial", 14))
        self.disk_button.grid(row=0, column=0)

        self.spiral_arms_button = Checkbutton(natural_residuals, text="Spiral Arms", wraplength=90,
                                              command=self.spiral_arms, font=("Arial", 14))
        self.spiral_arms_button.grid(row=0, column=1)

        self.gal_bar_button = Checkbutton(natural_residuals, text="Bar", wraplength=90,
                                          command=self.bar, font=("Arial", 14))
        self.gal_bar_button.grid(row=0, column=2)

        self.global_other_button = Checkbutton(natural_residuals, text="Other",
                                                        wraplength=90,
                                                        command=self.global_other, font=("Arial", 14))
        self.global_other_button.grid(row=1, column=0)

        self.asymmetric_fit_button = Checkbutton(natural_residuals, text="Asymmetric",
                                                 wraplength=90,
                                                 command=self.asymmetric, font=("Arial", 14))
        self.asymmetric_fit_button.grid(row=1, column=1)

        # Poor Fit Artifacts

        self.diffraction_spikes_button = Checkbutton(artifacts, text="Diffraction Spikes",
                                                     wraplength=90,
                                                     command=self.diffraction_spikes, font=("Arial", 14))
        self.diffraction_spikes_button.grid(row=0, column=0)

        self.image_edge_button = Checkbutton(artifacts, text="Image Edge",
                                             wraplength=90,
                                             command=self.image_edge, font=("Arial", 14))
        self.image_edge_button.grid(row=0, column=1)

        self.unfit_neighbor_button = Checkbutton(artifacts, text="Unfit\n Neighbor",
                                             wraplength=90,
                                             command=self.unfit_neighbor, font=("Arial", 14))
        self.unfit_neighbor_button.grid(row=0, column=2)

        # Tidal Features

        self.tidal_features_present_button = Checkbutton(tidal_features, text="Strong", wraplength=90,
                                                         command=self.tidal_features_pres, font=("Arial", 14))
        self.tidal_features_present_button.grid(row=0, column=0)

        self.tidal_features_possible_button = Checkbutton(tidal_features, text="Possible",
                                                          wraplength=90,
                                                          command=self.tidal_features_poss, font=("Arial", 14))
        self.tidal_features_possible_button.grid(row=0, column=1)

        # Done Button

        self.Done_button = Button(master_frame, text="Done !", wraplength=55, command=self.done, font=("Arial", 14))
        self.Done_button.pack(side=RIGHT, anchor=E, padx=10)

        #Save and Exit Button
        self.save_and_exit_button = Button(save, text="Save & Exit", wraplength=90, command = self.save_and_exit, font=("Arial", 14))
        self.save_and_exit_button.pack(side=LEFT)

        # Image Frame

        self.canvas = FigureCanvasTkAgg(fig, master=master)
        self.canvas.get_tk_widget().pack()

    def clean_residual(self):
        self.newgal.clean_residual = 1
        self.decision = self.newgal.makecsvline()
        self.root.destroy()

    def bright_center(self):
        if self.newgal.bright_center == 0:
            self.newgal.bright_center = 1
        elif self.newgal.bright_center == 1:
            self.newgal.bright_center = 0

    def dark_ring(self):
        if self.newgal.dark_ring == 0:
            self.newgal.dark_ring = 1
        elif self.newgal.dark_ring == 1:
            self.newgal.dark_ring = 0

    def dark_center(self):
        if self.newgal.dark_center == 0:
            self.newgal.dark_center = 1
        elif self.newgal.dark_center == 1:
            self.newgal.dark_center = 0

    def bright_ring(self):
        if self.newgal.bright_ring == 0:
            self.newgal.bright_ring = 1
        elif self.newgal.bright_ring == 1:
            self.newgal.bright_ring = 0

    def core_other(self):
        if self.newgal.core_other == 0:
            self.newgal.core_other = 1
        elif self.newgal.core_other == 1:
            self.newgal.core_other = 0

    def disk(self):
        if self.newgal.disk == 0:
            self.newgal.disk = 1
        elif self.newgal.disk == 1:
            self.newgal.disk = 0

    def spiral_arms(self):
        if self.newgal.spiral_arms == 0:
            self.newgal.spiral_arms = 1
        elif self.newgal.spiral_arms == 1:
            self.newgal.spiral_arms = 0

    def global_other(self):
        if self.newgal.global_other == 0:
            self.newgal.global_other = 1
        elif self.newgal.global_other == 1:
            self.newgal.global_other = 0

    def bar(self):
        if self.newgal.bar == 0:
            self.newgal.bar = 1
        elif self.newgal.bar == 1:
            self.newgal.bar = 0

    def asymmetric(self):
        if self.newgal.asymmetric == 0:
            self.newgal.asymmetric = 1
        elif self.newgal.asymmetric == 1:
            self.newgal.asymmetric = 0

    def diffraction_spikes(self):
        if self.newgal.diffraction_spikes == 0:
            self.newgal.diffraction_spikes = 1
        elif self.newgal.diffraction_spikes == 1:
            self.newgal.diffraction_spikes = 0

    def image_edge(self):
        if self.newgal.image_edge == 0:
            self.newgal.image_edge = 1
        elif self.newgal.image_edge == 1:
            self.newgal.image_edge = 0

    def unfit_neighbor(self):
        if self.newgal.unfit_neighbor == 0:
            self.newgal.unfit_neighbor = 1
        elif self.newgal.unfit_neighbor == 1:
            self.newgal.unfit_neighbor = 0

    def tidal_features_pres(self):
        if self.newgal.tidal_features_pres == 0:
            self.newgal.tidal_features_pres = 1
        elif self.newgal.tidal_features_pres == 1:
            self.newgal.tidal_features_pres = 0

    def tidal_features_poss(self):
        if self.newgal.tidal_features_poss == 0:
            self.newgal.tidal_features_poss = 1
        elif self.newgal.tidal_features_poss == 1:
            self.newgal.tidal_features_poss = 0

    def done(self):
        if self.newgal.add_all() > 0:
            self.decision = self.newgal.makecsvline()
            self.root.destroy()

        if self.newgal.add_all() == 0:
            tkMessageBox.showwarning('Error', 'No options were chosen. Please choose an option and try again!')
            self.root.mainloop()

    def save_and_exit(self):
        self.breakout =1
        self.root.destroy()


# allow the user to call any folder they want
parser = OptionParser()

parser.add_option("-c", "--csv",
                  action="store", type="string", dest="csvfile")

parser.add_option("-f", "--filepath",
                  action="store", type="string", dest='path')

options,args = parser.parse_args()

path = str()
if options.path == None:
    path = os.getcwd()
else:
    path = options.path

directory = os.listdir(os.getcwd())

if options.csvfile in directory:
    sample = glob.glob(path + '/*.fits')

    IDS = []
    for filepath in sample:
        head,tail = os.path.split(filepath)
        IDS.append(tail)

    oldcsv = np.genfromtxt(options.csvfile, names=True, dtype=None, delimiter=',')
    for each in oldcsv:
        if each['ID'] in IDS:
            sample.remove(path + each['ID'])

    newcsv = open(options.csvfile, 'a')
    for each in sample:
        _, id = os.path.split(each)
        newcsv.write(emulate_image(each, id))
    newcsv.close()

elif options.csvfile not in directory:


    csvheader = 'ID, Clean Residual, Bright Center, Dark Center, Bright Ring, Dark Ring, Striped, Artifact, Disk, Substructure, Spiral Arms, Asymmetric, Bar, Diffraction Spikes, Image Edge, Tidal Features Pres, Tidal Features Poss'
    newfilename = options.csvfile
    sample = glob.glob(path + '/*.fits')

    newcsv = open(newfilename, 'w')
    newcsv.write(csvheader)
    newcsv.write('\n')
    newcsv.close()

    newcsv = open(newfilename, 'a')
    for each in sample:
        _, id = os.path.split(each)
        newcsv.write(emulate_image(each, id))

    newcsv.close()
