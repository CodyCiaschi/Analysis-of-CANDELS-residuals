from sys import argv
import numpy as np
import astropy.io.ascii as ascii
from astropy.table import Table
import matplotlib.pyplot as plt
import os
from shutil import copyfile

csv1 = argv[1]
csv2 = argv[2]

csv1_data = ascii.read(csv1)
csv2_data = ascii.read(csv2)
'''
ID1 = csv1_data['ID']
ID2 = csv2_data['ID']

del csv1_data['ID']
del csv2_data['ID']
'''

total_class = len(csv1_data)
spec_diff = np.array([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0])
diff_total = 0.0

for row1,row2 in zip(csv1_data,csv2_data):
    diff = []
    for i in range(1,16):
        diff_val = row1[i] - row2[i]
        diff.append(diff_val)
    
    diff = np.array(diff)
    if np.sum(diff) == 0:
        diff_total += 1
    elif np.sum(diff) != 0: #copy image to diff folder
        copyfile('/Users/cpcyr8/Desktop/GOODS_S_clump_1/%s'%(row1['ID']),'/Users/cpcyr8/Desktop/codyrubygoods_s_1_diff/%s'%(row1['ID']))



    index = np.where(diff == 0)

    if len(index[0]) != 0:
        spec_diff[index] += 1

total_diff = (diff_total/total_class) * 100.0
spec_diff = (spec_diff/total_class) * 100

stdev = np.sqrt(spec_diff)

newtable = Table(names=('Clean_Residual', 'Bright_Center', 'Dark_Center', 'Bright_Ring', 'Dark_Ring', 'Core_Other', 'Disk', 'Global_Other', 'Asymmetric', 'Bar', 'Diffraction_Spikes', 'Image_Edge', 'Unfit_Close_Companion', 'Tidal_Features_Present', 'Tidal_Features_Possible'))
newtable.add_row(spec_diff)

print newtable
print 'Total Difference = %5.2f %s'%(total_diff,'%')

_,tail1 = os.path.split(csv1)
_,tail2 = os.path.split(csv2)


ind = np.arange(15)
fig = plt.figure(figsize=[10,8])
ax = plt.gca()
ax.errorbar(ind, spec_diff, color='black',yerr=stdev,marker='o',ecolor='black',capsize=2,linestyle='None')
ax.set_xticklabels(('Clean', 'BR_Center', 'Dk_Center', 'BR_Ring', 'Dk_Ring', 'Core_Other', 'Disk', 'Global_Other', 'Asymmetric', 'Bar', 'Diff_Spikes', 'Img_Edge', 'Unfit_Comp', 'Tidal_Pres', 'Tidal_Poss'),rotation=45)
ax.text(0.25, 10, 'csv files compared: %s & %s \ntotal agreement: %5.1f%s' %(tail1,tail2,total_diff,'%'), style='italic', bbox={'facecolor':'white', 'alpha':0.5, 'pad':10})
ax.set_xticks(ind)
ax.set_ylim(0,115)
ax.errorbar = stdev
ax.tick_params(labeltop = True)
ax.xaxis.set_ticks_position('both')
ax.axhline(80, linestyle = '--', color='black')
plt.ylabel('Percent Agreement(agreement in column/total galaxies')

plt.show()