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
from sklearn.preprocessing import LabelEncoder

# loading our tracks and labels
t_l_file = "TracksIds_Labels.txt"
train_labels_file = "train_labels.txt"
test_labels_file = "test_labels.txt"

def one_vs_all_list(labels, limit_to):
    new_labels = []
    for lbl in labels:
        new_labels.append(lbl if lbl == limit_to else limit_to+1)
    return new_labels

def cross_validate_svm_one_vs(data, labels):
    # trying rock vs all first
    rock_vs_all = np.array(one_vs_all_list(labels, 1))
    clf = svm.SVR(kernel='poly')
    print data.shape
    print rock_vs_all.shape
    scores = cross_val_score(clf, data, rock_vs_all, cv=5)
    print scores

def cross_validate_svm(data, labels):
    clf = svm.SVR(kernel='poly')
    # f1 may work
    scores = cross_val_score(clf, data, labels, cv=5)
    print scores

def cross_validate_nn(data, labels):
    return 0

def main():
    if len(sys.argv) < 2:
        print "Please provide some arguments"
        sys.exit(1)

    lb = LabelEncoder()
    # for cross validation
    if sys.argv[1] == "--cross":
        if len(sys.argv) != 3 or not os.path.isfile(sys.argv[2]):
            print "Please provide the training set"

        train_labels = load_labels_text(train_labels_file)

        # getting only the labels
        train_labels = lb.fit_transform([x[1] for x in train_labels])
        train_data = load_array(sys.argv[2])

        # put some fitting stuff here
        print "Cross validating"
        cross_validate_svm(train_data, train_labels)

    elif sys.argv[1] == "--test":
        print "Please provide the test set and train set"
        train_labels = load_labels_text(train_labels_file)
        train_labels = lb.fit_transform([x[1] for x in train_labels])
        test_labels = load_labels_text(test_labels_file)
        test_labels = lb.fit_transform([x[1] for x in test_labels])

        print "Training and testing"

    return 0

if __name__=="__main__":
    main()