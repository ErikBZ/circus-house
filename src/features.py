# import the usual suspects
import numpy as np
import os
import sys
import datetime
import paths

# importing hdf5
import hdf5_getters as hdf5

# creates a group of features
feature_list = []

# should always be called if we're trying to extract
# new features
def clean_feature():
    # clearing the feature list
    feature_list[:] = []

# this should be passed into the apply to all function
# extract from h5
def extract_features(filename):
    h5 = hdf5.open_h5_file_read(filename)
    feature_vector = []
    feature = hdf5.get_sections_start(h5)
    feature_vector.append(feature.shape)
    feature = hdf5.get_sections_confidence(h5)
    feature_vector.append(feature.shape)
    feature = hdf5.get_segments_pitches(h5)
    feature_vector.append(feature)

    feature_list.append(feature_vector)

    h5.close()