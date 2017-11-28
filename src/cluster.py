# cluster the 10000 subset items to figure out which terms
# which 20ish genres

import os
import sys
import time
import glob
import datetime
import tables
import numpy as np
import paths
from features import *

#sklearn stuff here
from sklearn.cluster import KMeans

# according to wikipedia these are the most popular genres
    #Blues
    #Country
    #Easy(new age/elevator)
    #Electronic
    #Folk
    #Hip-Hop
    #Jazz
    #Latin
    #Pop
    #Soul
    #Rock
#k=11 i guess

extract()
if os.path.exists("feature_data.npy"):
    print "Loading data"
    features = load_array()
else:
    print "Do data, please create"
    sys.exit(0)

# load labels
if os.path.exists("targets.npy"):
    print "Loading targets"
    targets = load_array("targets.npy")
else:
    print "No targets npy array found, creating"
    apply_to_all_files(paths.msd_subset_data_path, func=extract_targets)
    targets = np.array(feature_list)
    save_features(targets, "targets.npy")
    clear_wrapper()

# i'll be trying DBScan and K-Means, maybe agglomerative
# first k-Means

# list of dictionaries containing the targets
grouped_terms = [{} for x in range(11)]

cluster = KMeans(n_clusters=11).fit(features)
arr = cluster.labels_
# going to save it into file with a certain name
folder = "kmeans"

print "Counting the terms"
for i in xrange(len(arr)):
    label = arr[i]
    for word in targets[i]:
        # adding it to the tracker
        if word in grouped_terms[label]:
            grouped_terms[label][word] += 1
        else:
            grouped_terms[label][word] = 1

print "Saving items into files"
def write_dict_to_array(data, filename):
    with open(os.path.join(folder, filename), "w") as f:
        for d in data:
            if data[d] > 1:
                f.write("{0}: {1}\n".format(d, data[d]))

for i in xrange(len(grouped_terms)):
    write_dict_to_array(grouped_terms[i], str(i))