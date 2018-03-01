'''
This Program creates randomly sampled Training, Validation and Testing Set from folders of different classes. Such as "house" and "not house".
'''
import shutil
import random
import numpy as np
import sys, os


# Constants needed for sampling
TRAIN_SIZE = 20000
VAL_SIZE = 1000
TEST_SIZE = 1000

# check for enough arguments
if len(sys.argv) != 2:
    print("Need path to folder containing subdirectories. Such as path to folder called 'all_houses', and 'all_houses' contains subdirectories 'house' and 'not_house'...")
    sys.exit(1)

# folder which contains the sub directories
source_dir = sys.argv[1]

# list sub directories
for root, dirs, files in os.walk(source_dir):

    # Iterate through each directory. (House and Not house)
    for i in dirs:

        # Create a new folder with the name of the iterated sub dir. This wil make a training, validation and test folder, all of which will be inside directory 'house_Images_resampled'
        path_train = source_dir + '/house_Images_resampled/training/train_' + "%s/" % i
        path_val = source_dir + '/house_Images_resampled/validation/val_' + "%s/" % i
        path_test =source_dir + '/house_Images_resampled/testing/test_' + "%s/" % i
        os.makedirs(path_train)
        os.makedirs(path_val)
        os.makedirs(path_test)

        # Take random sample of files per sub dir for Training set
        train_names = random.sample(os.listdir(source_dir + "%s/" % i ), TRAIN_SIZE)

        # Take files all files in directory
        files_in_dir = (os.listdir(source_dir + "%s/" % i ))

        # Get files not in training set so that we can sample these for validation set
        files_in_dir = np.asarray(files_in_dir)
        potential_val_files = []
        for f in files_in_dir:
            if f not in train_names:
                potential_val_files.append(f)

        # Randomly sample files that were not used in training to be used in validation set.
        val_files = random.sample(potential_val_files, VAL_SIZE)

        # Create a testing set. (files not sampled in training or validation. We want these to be unseen!)
        potential_test_files = []
        for f in files_in_dir:
            if f not in train_names and f not in val_files:
                potential_test_files.append(f)

        # Randomly sample to get test set
        test_files = random.sample(potential_test_files, TEST_SIZE)

        # Copy the files to the new destination. Training, Validation and Test
        for j in train_names:
            shutil.copy2(source_dir + "%s/" % i + j, path_train)

        for j in val_files:
            shutil.copy2(source_dir + "%s/" % i + j, path_val)

        for j in test_files:
            shutil.copy2(source_dir + "%s/" % i + j, path_test)










''''EX path:
source_dir = /Users/ee9w/Documents/skyScout/Cornerstone Sample/ShapeFiles_Houses_Mass/Boston/resample_houses_total/'
'''