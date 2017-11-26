#!/usr/bin/python
# the ususal suspects
import os
import sys
import time
import glob
import datetime
import sqlite3
import tables
# don't know why people do it this way but
# whatever.
import numpy as np
import paths
from features import *

def strimedelta(startime, stoptime):
    return str(datetime.timedelta(seconds=stoptime-startime))

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

def str_time_delta(starttime, stoptime):
    return str(datetime.timedelta(seconds=stoptime - starttime))

print apply_to_all_files(paths.msd_subset_data_path, func=extract_features)
feature_vector = [x for x in feature_list]
data = np.array(feature_vector)
print data.shape

minSegments = sys.maxint
for d in data:
    print d.shape