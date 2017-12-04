#! /usr/bin/python
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
import heapq
from features import *

#sklearn stuff here
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering

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
# according to the MSD it's 10 and GZTAN
    # Classic Pop and Rock
    # Folk
    # Dance
    # Electronica
    # Jazz and Blues
    # Soul and Reggae
    # Punk
    # Metal
    # Clasical
    # Pop
    # Hip-Hop
#k=11 i guess

# getting the top 5 words of each
sys.stderr = open("error.log", "w") 
def get_top_five(data):
    heap = []
    result = []
    for d in data:
        heapq.heappush(heap, (-1*data[d], d))
    for i in xrange(5):
        if i < len(heap):
            score, key = heapq.heappop(heap)
            result.append((key, score*-1))
    return result

def write_dict_to_array(data, filename):
    with open(os.path.join(folder, filename), "w") as f:
        for d in data:
            if data[d] > 1:
                f.write("{0}: {1}\n".format(d, data[d]))

# trying kmeans from 1 - 20
# trying 3 times
def kmeans():
    if os.path.exists("Segs_Timbre_Features.npy"):
        print "Loading data"
        features = load_array("Segs_Timbre_Features.npy")
    else:
        print "No data, please create"
        sys.exit(1)

    # load labels
    if os.path.exists("MBTags_Targets.npy"):
        print "Loading targets"
        targets = load_array("MBTags_Targets.npy")
    else:
        print "No targets array"
        sys.exit(1)

    # i'll be trying DBScan and K-Means, maybe agglomerative
    # first k-Means
    # trying for 20 clusters
    for i in xrange(20):
        # list of dictionaries containing the targets
        grouped_terms = [{} for x in range(i+1)]
        k_cluster = i+1

        cluster = KMeans(n_clusters=k_cluster).fit(features)
        # use this to get some metrics on the labels
        arr = cluster.labels_
        # this is the best inertia I believe
        error = cluster.inertia_

        # going to save it into file with a certain name
        folder = "kmeans_feat2"

        print "Counting the terms"
        for i in xrange(len(arr)):
            label = arr[i]
            for word in targets[i]:
                # adding it to the tracker
                if word in grouped_terms[label]:
                    grouped_terms[label][word] += 1
                else:
                    grouped_terms[label][word] = 1

        print "Getting top five words per cluster"
        top_words_for_each_cluster = []
        for i in xrange(len(grouped_terms)):
            top_five = get_top_five(grouped_terms[i])
            top_words_for_each_cluster.append(top_five)

        print "Writing info to file"
        filename = "k_mean_k={0}_try={1}.txt".format(k_cluster, 0)
        with open(os.path.join(folder, filename), "w") as f:
            f.write("K Means with K = {0}\n".format(k_cluster))
            f.write("Best Error: {0}\n\n".format(error))
            for i in xrange(len(grouped_terms)):
                f.write("Top Words for Label: {0}\n".format(i))
                words = top_words_for_each_cluster[i]
                for word in words:
                    key, score = word            
                    f.write("{0}: {1}\n".format(key, score))
                f.write("\n\n")

def agglo():
    return 0

if __name__=="__main__":
    if len(sys.argv) != 2:
        sys.exit()
    if sys.argv[1] == "-k":
        kmeans()
    elif sys.argv[1] == "-a":
        agglo()