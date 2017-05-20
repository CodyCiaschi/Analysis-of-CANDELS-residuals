from Tkinter import *
from PIL import ImageTk, Image
from collections import defaultdict
import numpy as np
import os
from time import gmtime, strftime
def emulate_image(file_path,gal_id,field):
    class App:
    
        def __init__(self, master):
    
            frame = Frame(master)
            frame.pack()
            self.decision = defaultdict(list)
            self.status = {'star_button':'inactive','on_edge_ok_button':'inactive','on_edge_n_ok_button':'inactive','diff_spike_button':'inactive','maybe_star_button':'inactive','close_star_button':'inactive','false_flag_button':'inactive'}
            self.star_button = Checkbutton(frame, text="Star", command=self.star)
            self.star_button.pack(side=LEFT)
            
            self.on_edge_n_ok_button = Checkbutton(frame, text="On edge\n but not okay",wraplength=75, command=self.on_edge_not_ok)
            self.on_edge_n_ok_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)
            
            self.on_edge_ok_button = Checkbutton(frame, text="On edge\n and okay",wraplength=55, command=self.on_edge_ok)
            self.on_edge_ok_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)
            
            self.diff_spike_button = Checkbutton(frame, text="On Diffraction Spike",wraplength=65, command=self.diff_spike)
            self.diff_spike_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)
            
            self.maybe_star_button = Checkbutton(frame, text="Maybe a star\n Needs inspection",wraplength=75, command=self.needs_inspection)
            self.maybe_star_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)
            
            self.close_star_button = Checkbutton(frame, text="Near a star\n Possible Contamination",wraplength=90, command=self.close_star)
            self.close_star_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)
            
            self.bad_pix_button = Checkbutton(frame, text="Near/Has\n Bad pixels",wraplength=75, command=self.bad_pix)
            self.bad_pix_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)
            
            self.false_flag_button = Checkbutton(frame, text="Falsly Flagged",wraplength=75, command=self.false_flaged)
            self.false_flag_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)
                        
            self.Done_button = Button(frame, text="Done !",wraplength=55, command=self.done)
            self.Done_button.pack(side=LEFT,expand = 1, padx = 10, pady = 10)
        
        def activate(button,self):
                self.status[button]='active'
        def deactive(button,self):
            self.status[button]='inactive'
            
        def star(self):
            if 'S' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('S')
            elif 'S' in self.decision['%s'%gal_id] :
                self.decision['%s'%gal_id].remove('S')
        def on_edge_not_ok(self):
            if 'OE_N' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('OE_N')
            elif 'OE_N' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('OE_N')
        def on_edge_ok(self):
            if 'OE_K' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('OE_K')
            elif 'OE_K' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('OE_K')
                pass
        
        def diff_spike(self):
            if 'DS' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('DS')
            elif 'DS' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('DS')
        
        def needs_inspection(self):
            if 'NI' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('NI')
            elif 'NI' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('NI')
        def close_star(self):
            if 'PC' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('PC')
            elif 'PC' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('PC')
        def false_flaged(self):
            if 'FF' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('FF')
            elif 'FF' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('FF')
        def bad_pix(self):
            if 'BP' not in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].append('BP')
            elif 'BP' in self.decision['%s'%gal_id]:
                self.decision['%s'%gal_id].remove('BP')
                
        def done(self):
            if self.decision['%s'%gal_id] != []:
                root.destroy()
            if self.decision['%s'%gal_id] == []:
                self.decision['%s'%gal_id].append('OK')
                root.destroy()
    root = Tk()
    app = App(root)
    root.geometry("+{}+{}".format(20,50))
    root.title("show multiple images")
    
    imageFile1 = file_path+'%s_ID_%s_pix.png' %(field,gal_id)
    imageFile2 = file_path+'%s_ID_%s_kpc.png' %(field,gal_id)
    
    image1 = Image.open(imageFile1).resize((700, 500))
    image2 = Image.open(imageFile2).resize((700, 500))
    # PIL's ImageTk converts to an image object that Tkinter can handle
    photo1 = ImageTk.PhotoImage(image1)
    photo2 = ImageTk.PhotoImage(image2)
    
    
    
    # put the image objects on labels in a grid layout
    label1= Label(root,image=photo1)
    label1.grid(row=0, column=0)
    label1.pack(side="right")
    
    label2 = Label(root,image=photo2)
    label2.grid(row=1, column=0)
    label2.pack(side="left")
    
    
    
    
    
    root.mainloop()
    return(app.decision)


def scan_current_folder():
    list_of_files=os.listdir(os.getcwd())
    list_of_id=[]
    for each in list_of_files:
        if each.endswith('.png'):
            if each.split('_')[2] == 'kpc.png':
                gal_id = int(each.split('_')[1])
                list_of_id.append(gal_id)
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
new_decision_dict = dict()
for each in random_sample:
    this_decision=emulate_image(os.getcwd()+'/',each,'CMS')
    for galaxy,flags in this_decision.items():
        flag_string = str()
        for each in flags:
            flag_string = flag_string+each+'/'
        new_decision_dict[galaxy] = flag_string
print new_decision_dict

final_information_array=[['ID','Visual_check_flag']]
for key,value in new_decision_dict.items():
    final_information_array.append([key,value])
writeCsvFile(os.getcwd()+'/classification_results_%s.csv'%(strftime("%Y-%m-%d %H:%M:%S", gmtime())),final_information_array)