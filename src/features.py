#! /usr/bin/python
# import the usual suspects
import numpy as np
import os
import sys
import datetime
import paths
import glob

# importing hdf5
import hdf5_getters as hdf5

# min segments
minSegments = 100
numberOfEntries = 10000

# creates a group of features
# should be in a (n_samples, n_features) shape
# so all samples should have the same number of features
feature_list = []
entries = np.zeros((numberOfEntries, minSegments * 12), dtype=float)

#this function iterates through all the files and applies a function lambda
def apply_to_all_files(basedir, func= lambda x: x, ext=".h5"):
    cnt = 0
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root, '*'+ ext))
        # this is walking through the folders so it has to count up the files in
        # each of the folders
        cnt += len(files)
        for f in files:
            func(f)
    return cnt

# should always be called if we're trying to extract
# new features
def clear_wrapper():
    # clearing the feature list
    feature_list[:] = []

# this should be passed into the apply to all function
# extract from h5
# this feature list will only use the first 100 segments of a
# song. I can try with more
def extract_features(filename):
    h5 = hdf5.open_h5_file_read(filename)

    # segments are the mfcc like features
    full_array = hdf5.get_segments_pitches(h5)[:100]
    # flat array for features
    # only testing first 100 segments of any given song
    first_100_slice = np.zeros((minSegments, 12))
    first_100_slice[:full_array.shape[0], :full_array.shape[1]] = full_array
    feature = np.resize(first_100_slice, minSegments * 12) 
    feature_list.append(feature)

    h5.close()

def extract_beats(filename):
    return 0

def extract_targets(filename):
    h5 = hdf5.open_h5_file_read(filename)

    # getting the target classes for the stuff
    # only 12 terms
    # for now we'll just use the first one
    terms = hdf5.get_artist_terms(h5)
    feature_list.append(terms)

    h5.close()

def save_features(feats, path="feature_data.npy"):
    np.save(path, feats)

def load_array(filename="feature_data.npy"):
    return np.load(filename)

def extract():
    # if these are truly not here, create them
    if not os.path.exists("feature_data.npy"):
        print "Creating features file"
        apply_to_all_files(paths.msd_subset_data_path, func=extract_features)
        features = np.array(feature_list)
        save_features(features)
        clear_wrapper()

    if not os.path.exists("targets.npy"):
        print "Creating targets file"
        apply_to_all_files(paths.msd_subset_data_path, func=extract_targets)
        targets = np.array(feature_list)
        save_features(targets, "targets.npy")
        clear_wrapper()

def main():
    extract()

# this will be a mix of segments and beats?
if __name__=="__main__":
    main()