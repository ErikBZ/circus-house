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

# loading our tracks and labels
t_l_file = "TracksIds_Labels.txt"

def main():
    tracks_labels = load_labels_text(t_l_file)
    labels = [x[1] for x in tracks_labels]
    return 0

if __name__=="__main__":
    main()