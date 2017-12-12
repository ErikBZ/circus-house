#!/usr/bin/python
# does the actual mining 
import os
import sys
import time
import glob
import datetime
import tables
import numpy as np
import paths
from features import *

#sklearn stuff
from sklearn.model_selection import cross_val_score
from sklearn import svm
from sklearn import neighbors

# extract()
extract_2()
# mining goes here
if os.path.exists("Loudness_Features.npy"):
    print "Loading features"
    features = load_array("Loudness_Features.npy")
else:
    print "No features found"
    sys.exit(1)

if os.path.exists("MBTags_Targets.npy"):
    print "Loading targets"
    targets = load_array("MBTags_Targets.npy")
else:
    print "No targets file found"
    sys.exit(1)

index_map, targets = set_correct_tag(targets)
# filter out items in features
features_to_use = np.zeros((len(targets), features.shape[1]))
true_targs = np.array(targets)

def map_items(mapping, features, out_feats):
    for x in mapping:
        out_feats[mapping[x]] = features[x]

map_items(index_map, features, features_to_use)

print "Targets and features loading complete"
print len(features_to_use)

# start the cross validation here
clf = svm.SVC(kernel='linear', C=1.0)
scores = cross_val_score(clf, features_to_use, true_targs, cv=5)
print scores
'''
for i in xrange(1, 13, 2):
    clf = neighbors.KNeighborsClassifier(n_neighbors=i)
    scores = cross_val_score(clf, features_to_use, true_targs, cv=5)
    print scores
'''