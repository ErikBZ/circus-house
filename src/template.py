#!/bin/bash/python
# the ususal suspects
import os
import sys
import time
import glob
import datetime
import sqlite3
# don't know why people do it this way but
# whatever.
import numpy as np

msd_subset_path = "/home/flipper/Documents/circus-house/MillionSongSubset"
msd_subset_data_path = os.path.join(msd_subset_path, "data")
msd_subset_addf_path = os.path.join(msd_subset_path, "AdditionalFiles")
# no highway to the danger zone
assert os.path.isdir(msd_subset_path), "No Path"
# my code bruh
msd_code_path = "/home/flipper/Documents/circus-house/src/"

import hdf5_getters as GETTERS

def strimedelta(startime, stoptime):
    return str(datetime.timedelta(seconds=stoptime-startime))

#this function iterates through all the files and applies a function lambda
def apply_to_all_files(basedir, func= lambda x: x, ext=".h5"):
    cnt = 0
    for root, dirs, files in os.walk(basedir):
        files = glob.glob(os.path.join(root, '*'+ ext))
        cnt = len(files)
        for f in files:
            func(f)
    return cnt