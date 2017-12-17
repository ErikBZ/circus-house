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
from sklearn.preprocessing import normalize
from sklearn.pipeline import Pipeline
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel

# loading our tracks and labels
t_l_file = "TracksIds_Labels.txt"
train_labels_file = "train_labels.txt"
test_labels_file = "test_labels.txt"

def one_vs_all_list(labels, limit_to):
    new_labels = []
    for lbl in labels:
        new_labels.append(1 if lbl == limit_to else 0)
    return new_labels

def cull_features(data, labels):
    print "Culling Features"
    culler = ExtraTreesClassifier(n_estimators=200)
    culler = culler.fit(data, labels)
    model = SelectFromModel(culler, prefit=True)
    return model

# use regression for this?
def cross_validate_svm_one_vs(data, labels):
    # culling data just once
    # trying rock vs all first
    for i in range(10):
        rock_vs_all = np.array(one_vs_all_list(labels, i))
        new_data = cull_features(data, rock_vs_all).transform(data)
        print new_data.shape
        clf = svm.SVC(kernel='poly', C=4.0)
        scores = cross_val_score(clf, new_data, rock_vs_all, cv=5, scoring='f1')
        print scores

def cross_validate_svm(data, labels):
    print "Normalizing"
    normalize(data, norm='l1', axis=1, copy=True)
    new_data = cull_features(data, labels).transform(data)
    print new_data.shape
    clf = svm.SVC(C=4.0, kernel='poly')
    print "Validating svm"

    # f1 may work
    # does not take unbalance into consideration
    scores = cross_val_score(clf, new_data, y=labels, cv=5)
    print scores

def predict_nn(data, labels, test):
    return 0

def cross_val_knn(data, labels, k_max):

    return 0

# gets the f1 score of each
# label unweighted
def score(ground, predict, label_mapping):
    labels = label_mapping.inverse_transform(ground)
    # 0 = All True Pos, 1 = Correctly Guessed Postives, 2 = All Guessed Pos
    counts = {}
    for i in xrange(len(ground)):
        lbl = ground[i]
        if lbl not in counts:
            counts[lbl] = [0,0,0]
        if predict[i] not in counts:
            counts[predict[i]] = [0,0,0]

        counts[lbl][0] += 1 
        if lbl == predict[i]:
            counts[lbl][1] += 1
        else:
            counts[predict[i]][2] += 1
        # do something here

    for key in counts:
        label = get_label(ground, labels, key)
        all_pos = counts[key][0]
        true_pos = counts[key][1]
        false_pos = counts[key][2]
        f1 = f1_score(all_pos, true_pos, false_pos)
        print "{0}:".format(label)
        print "\t\t\tF1: {0:.2f}\t All Pos: {1}\t True Pos: {2}\t False Pos: {3}".format(
            f1, all_pos, true_pos, false_pos)

def compute_confusion(ground, predict):
    return 0

def f1_score(pos_elem, true_pos, false_pos):
    if true_pos + false_pos == 0:
        prec = 0
    else:
        prec = true_pos / float(true_pos + false_pos)
    # recall should never be 0
    recall = true_pos / float(pos_elem)
    denom = recall + prec if recall != 0 and prec != 0 else 1
    return 2 * (prec * recall)/(denom)

# gets the unicode label from the int translation
def get_label(ground, labels, int_label):
    index_of = 0
    for i in xrange(ground.shape[0]):
        if ground[i] == int_label:
            return labels[i]
    return ""

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
        cross_validate_svm_one_vs(train_data, train_labels)

    elif sys.argv[1] == "--test":
        if (len(sys.argv) != 4 or
            not os.path.isfile(sys.argv[2]) or
            not os.path.isfile(sys.argv[3])):
            print "Input files could not be found"
            print "Or Enter [test] [train] files"
            sys.exit(0)

        print "Please provide the test set and train set"
        train_labels = load_labels_text(train_labels_file)
        train_labels = lb.fit_transform([x[1] for x in train_labels])
        test_labels = load_labels_text(test_labels_file)
        test_labels = lb.fit_transform([x[1] for x in test_labels])

        train_data = load_array(sys.argv[3])
        test_data = load_array(sys.argv[2])

        model = cull_features(train_data, train_labels)
        train_culled = model.transform(train_data)
        test_culled = model.transform(test_data)

        print train_culled.shape
        print test_culled.shape
        print "Training and testing"

        # do fitting and predicting here
        clf = svm.SVC(C=5, kernel='poly')
        clf.fit(train_culled, train_labels)
        predictions = clf.predict(test_culled)

        '''
        clf = neighbors.KNeighborsClassifier(n_neighbors=11)
        clf.fit(train_culled, train_labels)
        predictions = clf.predict(test_culled)
        '''

        # score here
        score(test_labels, predictions, lb)
    return 0

if __name__=="__main__":
    main()