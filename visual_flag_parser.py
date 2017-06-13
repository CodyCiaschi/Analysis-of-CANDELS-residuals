import shutil
import numpy as np
import os

def parse_flags(csvname, path_to_files, original_catalog_name):

    info = np.genfromtxt(csvname, dtype=None, names=True, delimiter=',')

    if not os.path.exists('./%s_parsed_flags' %(original_catalog_name)):
        #make parent directory
        os.makedirs('./%s_parsed_flags'%(original_catalog_name))
        #make tidal features present directory
        os.makedirs('./%s_parsed_flags/tidal_features'%(original_catalog_name))
        #directories for TFP stuff
        os.makedirs('./%s_parsed_flags/tidal_features/good_residual' % (original_catalog_name))
        os.makedirs('./%s_parsed_flags/tidal_features/bad_residual_artifact' % (original_catalog_name))
        os.makedirs('./%s_parsed_flags/tidal_features/bad_residual_natural' % (original_catalog_name))
        os.makedirs('./%s_parsed_flags/tidal_features/reasonable_contains_clumps' % (original_catalog_name))
        os.makedirs('./%s_parsed_flags/tidal_features/reasonable_contains_substructure' % (original_catalog_name))

        #make tidal features not present directory
        os.makedirs('./%s_parsed_flags/tidal_features_not_present' % (original_catalog_name))

        #directories for TFNP stuff
        os.makedirs('./%s_parsed_flags/tidal_features_not_present/good_residual' % (original_catalog_name))
        os.makedirs('./%s_parsed_flags/tidal_features_not_present/bad_residual_artifact' % (original_catalog_name))
        os.makedirs('./%s_parsed_flags/tidal_features_not_present/bad_residual_natural' % (original_catalog_name))
        os.makedirs('./%s_parsed_flags/tidal_features_not_present/reasonable_contains_clumps' % (original_catalog_name))
        os.makedirs('./%s_parsed_flags/tidal_features_not_present/reasonable_contains_substructure' % (original_catalog_name))

    for each in info:
        filename = each['ID']
        flags = each['Visual_check_flag']

        array_of_flags = flags.split('/')

        if 'TFP' in array_of_flags:
            if 'GR' in array_of_flags:
                shutil.move('%s/%s'%(path_to_files, filename), './%s_parsed_flags/tidal_features/good_residual'%(original_catalog_name))
            elif 'BRA' in array_of_flags:
                shutil.move('%s/%s' % (path_to_files, filename), './%s_parsed_flags/tidal_features/bad_residual_artifact'%(original_catalog_name))
            elif 'BRN' in array_of_flags:
                shutil.move('%s/%s' % (path_to_files, filename), './%s_parsed_flags/tidal_features/bad_residual_natural'%(original_catalog_name))
            elif 'RCC' in array_of_flags:
                shutil.move('%s/%s' % (path_to_files, filename), './%s_parsed_flags/tidal_features/reasonable_contains_clumps'%(original_catalog_name))
            elif 'RCS' in array_of_flags:
                shutil.move('%s/%s' % (path_to_files, filename), './%s_parsed_flags/tidal_features/reasonable_contains_substructure'%(original_catalog_name))
        else:
            if 'GR' in array_of_flags:
                shutil.move('%s/%s'%(path_to_files, filename), './%s_parsed_flags/tidal_features/reasonable_contains_substructure'%(original_catalog_name))
            elif 'BRA' in array_of_flags:
                shutil.move('%s/%s' % (path_to_files, filename), './%s_parsed_flags/tidal_features_not_present/bad_residual_artifact'%(original_catalog_name))
            elif 'BRN' in array_of_flags:
                shutil.move('%s/%s' % (path_to_files, filename), './%s_parsed_flags/tidal_features_not_present/bad_residual_natural'%(original_catalog_name))
            elif 'RCC' in array_of_flags:
                shutil.move('%s/%s' % (path_to_files, filename), './%s_parsed_flags/tidal_features_not_present/reasonable_contains_clumps'%(original_catalog_name))
            elif 'RCS' in array_of_flags:
                shutil.move('%s/%s' % (path_to_files, filename), './%s_parsed_flags/tidal_features_not_present/reasonable_contains_substructure'%(original_catalog_name))


parse_flags('classification_results_2017-06-13 20:36:36.csv','/Users/cpcyr8/Documents/CANDELS/GDS/massive_bright_subset_for_test', 'GOODS-S')
