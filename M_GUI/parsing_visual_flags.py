import numpy as np
import cut_out_bad_flags_with_flag_map as co
import os

good_flags_full = []
files_in_folder_good=os.listdir('/Users/km4n6/Box Sync/bharath/Second Project/cutouts/GDN/good/')

for each in files_in_folder_good:
    if each.endswith('.csv'):
        good_visual_inspec_flags = np.genfromtxt('/Users/km4n6/Box Sync/bharath/Second Project/cutouts/GDN/good/%s'%(each), dtype=None ,names=True,delimiter =",")
        for every in good_visual_inspec_flags:
            good_flags_full.append([every['ID'],every['Visual_check_flag']])           

files_in_bad_folder=os.listdir('/Users/km4n6/Box Sync/bharath/Second Project/cutouts/GDN/bad/')
bad_flags_full=[]
for each in files_in_bad_folder:
    if each.endswith('.csv'):
        bad_visual_inspec_flags = np.genfromtxt('/Users/km4n6/Box Sync/bharath/Second Project/cutouts/GDN/bad/%s'%(each), dtype=None ,names=True,delimiter =",")
        for every in bad_visual_inspec_flags:
            bad_flags_full.append([every['ID'],every['Visual_check_flag']])

id_good_false_flagged =[]
good_false_flag_info=[]
for each in good_flags_full:
    flag = each[1]
    flags_split = flag.split('/')
    if '' in flags_split:
        flags_split.remove('')
    if 'FF' in flags_split or 'OK' not in flags_split:
        id_good_false_flagged.append(each[0])
        good_false_flag_info.append([each[0],flags_split])
#1- PS, 2- CFS, 3- E
hist_false_flags=[]
for gal_id,each in good_false_flag_info:
    if 'S' in each or 'NI' in each:
        hist_false_flags.append(1)
    elif 'DS' in each or 'PC' in each :
        hist_false_flags.append(2)
    elif 'BP' in each or 'OE_N' in each:
        hist_false_flags.append(3)

import matplotlib.pyplot as plt
figure = plt.figure()
histogram = plt.hist(hist_false_flags)
plt.show()

bad_false_flag_info=[]
id_bad_false_flagged=[]
for each in bad_flags_full:
    flag = each[1]
    flags_split = flag.split('/')
    if '' in flags_split:
        flags_split.remove('')
    if 'FF' in flags_split:
        id_bad_false_flagged.append(each[0])
        bad_false_flag_info.append([each[0],flags_split])

#egs ---- hlsp_candels_hst_wfc3_egs-tot-60mas_f160w_v1.0_drz.fits
#other ---- hlsp_candels_hst_wfc3_egs-tot_f160w_v1.0_drz.fits
image = '/Users/km4n6/Downloads/hlsp_candels_hst_wfc3_gn-tot-60mas_f160w_v1.0_drz.fits'
image_flag = '/Users/km4n6/Downloads/GDN_FlagH160_new.fits'

destination_ff_good = '/Users/km4n6/Box Sync/bharath/Second Project/cutouts/GDN/false_flags/good/'
destination_ff_bad = '/Users/km4n6/Box Sync/bharath/Second Project/cutouts/GDN/false_flags/bad/'

co.cut_out_massive_gals(image,image_flag,id_good_false_flagged,100,'kpc',destination_ff_good,'/Users/km4n6/Box Sync/bharath/Research/Research/Main Catalogs/May16/Massive_Compare_catalogs/GDN_barro_wuyts_updated.csv','GDN','False')
co.cut_out_massive_gals(image,image_flag,id_good_false_flagged,500,'pix',destination_ff_good,'/Users/km4n6/Box Sync/bharath/Research/Research/Main Catalogs/May16/Massive_Compare_catalogs/GDN_barro_wuyts_updated.csv','GDN','False')
#
co.cut_out_massive_gals(image,image_flag,id_bad_false_flagged,100,'kpc',destination_ff_bad,'/Users/km4n6/Box Sync/bharath/Research/Research/Main Catalogs/May16/Massive_Compare_catalogs/GDN_barro_wuyts_updated.csv','GDN','False')
co.cut_out_massive_gals(image,image_flag,id_bad_false_flagged,500,'pix',destination_ff_bad,'/Users/km4n6/Box Sync/bharath/Research/Research/Main Catalogs/May16/Massive_Compare_catalogs/GDN_barro_wuyts_updated.csv','GDN','False')

