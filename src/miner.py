#!/usr/bin/python
# does the actual mining 
import os
import sys
import time
import glob
import datetime
import tables
import numpy as numpy
import paths
from features import *

#sklearn stuff
from sklearn.model_selection import cross_val_score
from sklearn import svm

# mining goes here
if os.path.exists("feature_data.npy"):
    print "Loading features"
    features = load_array()
else:
    print "No features found, recreating features"
    apply_to_all_files(paths.msd_subset_data_path, func=extract_features)
    features = np.array(feature_list)
    save_features(features)
    clear_wrapper()
print "Features loading/creation complete"

if os.path.exists("targets.npy"):
    print "Loading targets"
    targets = load_array("targets.npy")
else:
    print "No targets npy array found, creating"
    apply_to_all_files(paths.msd_subset_data_path, func=extract_targets)
    targets = np.array(feature_list)
    save_features(targets, "targets.npy")
    clear_wrapper()
print "Targets loading/creation complete"

# start the cross validation here
clf = svm.SVC(kernel='linear', C=1)
scores = cross_val_score(clf, features, targets, cv=5)
print scores