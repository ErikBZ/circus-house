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

extract()
# mining goes here
if os.path.exists("feature_data.npy"):
    print "Loading features"
    features = load_array()
else:
    print "No features found"
    sys.exit(1)
if os.path.exists("targets.npy"):
    print "Loading targets"
    targets = load_array("targets.npy")
else:
    print "No targets file found"
    sys.exit(1)

print "Targets and features loading complete"

# start the cross validation here
'''
clf = svm.SVC(kernel='linear', C=1)
scores = cross_val_score(clf, features, targets, cv=5)
print scores
'''