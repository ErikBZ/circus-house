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

msd_subset_path = "/home/flipper/Documents/circus-house/MillionSongSubset"
msd_subset_data_path = os.path.join(msd_subset_path, "data")
msd_subset_addf_path = os.path.join(msd_subset_path, "AdditionalFiles")
# no highway to the danger zone
assert os.path.isdir(msd_subset_path), "No Path"
# my code bruh
msd_code_path = "/home/flipper/Documents/circus-house/MSongsDB"
sys.path.append(os.path.join(msd_code_path, "PythonSrc"))

import hdf5_getters as GETTERS

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

print "number of song files: ", apply_to_all_files(msd_subset_data_path)

# yay for bad practices!
feature_vector = []
# trying to use the hdf5 getters to get the stuff i need
def get_feature_vector(h5):
    tatum_confidence_vector = GETTERS.get_tatums_confidence(h5)
    feature_vector.append(tatum_confidence_vector)

tatums_start = []
def get_tatums(h5):
    tatum = GETTERS.get_tatums_start(h5)
    tatums_start.append(tatum)

def get_all_vectors(filename):
    h5 = GETTERS.open_h5_file_read(filename)
    get_feature_vector(h5)
    get_tatums(h5)
    h5.close()

apply_to_all_files(msd_subset_data_path, func=get_all_vectors)
feature = feature_vector[0]
tatums = tatums_start[0]
print type(feature)
print tatums
print "Size of tatum conf: {0}, Size of tatum start: {1}".format(len(feature), len(tatums))

feature = feature_vector[1]
tatums = tatums_start[1]
print type(feature)
print "Size of tatum conf: {0}, Size of tatum start: {1}".format(len(feature), len(tatums))


# this is all the sql stuff that i might use. It is a lot faster but I can't
# find the specs so idk what the rows are called
'''
# messing with the sql
conn = sqlite3.connect(os.path.join(msd_subset_addf_path, "subset_track_metadata.db"))
# DISTINCT is pretty self explanatory
query = "SELECT DISTINCT artist_name FROM songs"
response = conn.execute(query)
all_names = response.fetchall()

print type(all_names[1])
print all_names[1]

query = "SELECT * from songs"
response = conn.execute(query)
data = response.fetchall()

print data[0]

conn.close()
'''