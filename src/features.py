#! /usr/bin/python
# import the usual suspects
import numpy as np
import os
import sys
import datetime
import paths
import glob
sys.stderr = open("features_error.log", "w")

# importing hdf5
import hdf5_getters as hdf5

# min segments
minSegments = 200
numberOfEntries = 10000

# used to find the mim element
minimum = [sys.maxint]

# creates a group of features
# should be in a (n_samples, n_features) shape
# so all samples should have the same number of features
feature_list = []
entries = np.zeros((numberOfEntries, minSegments * 12), dtype=float)
# the tags that i want to use
top_tags = ["classic pop and rock", "folk",
            "electronica", "jazz and blues",
            "soul and reggae", "punk",
            "metal", "classical", "pop", "hip hop", ""]

tag_count = {}
for tag in top_tags:
    tag_count[tag] = 0

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

# lst should be a list of tuples of size 2
def apply_to_all_listed_files(basedir, lst, func=lambda x:x):
    for track_id, class_tag in lst:
        path = os.path.join(basedir, get_file_path(track_id))
        func(path)
    return 0

# gets the path and filename of the track id
def get_file_path(track_id):
    data_location = ""
    dirs = track_id[2:5]
    for d in dirs:
        data_location = os.path.join(data_location, d)
    return os.path.join(data_location, track_id+".h5")

# used for labels this way
def check_if_common_tag(terms):
    for i in range(len(terms)):
        if terms[i] in top_tags:
            return True
    return False

def get_most_counted_term(terms, count):
    assert len(terms) == len(count)
    max_index = -1
    max_count = 0
    for i in range(len(terms)):
        if terms[i] in tag_count and max_count < count[i]:
            max_index = i
            max_count = count[i]
    return terms[max_index] if max_index > -1 else ""

def count_instances_per_term(terms, count):
    term = get_most_counted_term(terms, count)
    # also counts how many unknowns there are
    tag_count[term] += 1
    return 0

def arrange_by_tag(filename):
    h5 = hdf5.open_h5_file_read(filename)
    terms = hdf5.get_artist_mbtags(h5)
    count = hdf5.get_artist_mbtags_count(h5)
    count_instances_per_term(terms, count)
    h5.close()

# gets track id of the song, and it's label according to
# get_most_counted term
# track id is also the file and location of the song
def get_labels(filename):
    h5 = hdf5.open_h5_file_read(filename)
    terms = hdf5.get_artist_mbtags(h5)
    count = hdf5.get_artist_mbtags_count(h5)
    class_tag = get_most_counted_term(terms, count)

    if class_tag != "":
        track_id = hdf5.get_track_id(h5)
        feature_list.append((track_id, class_tag))

    h5.close()

def save_list_to_text(lst, filename):
    with open(filename, "w") as fout:
        for class_id, tag in lst:
            fout.write("{0},{1}\n".format(class_id, tag))

def load_labels_text(filename):
    labels = []
    with open(filename, "r") as fin:
        data = fin.readlines()
    for line in data:
        line = line.strip()
        id_label = line.split(',')
        labels.append((id_label[0], id_label[1]))
    return labels

# should always be called if we're trying to extract
# new features
def clear_wrapper():
    # clearing the feature list
    feature_list[:] = []

# this should be passed into the apply to all function
# extract from h5
# this feature list will only use the first 100 segments of a
# song. I can try with more
def extract_features(filename):
    h5 = hdf5.open_h5_file_read(filename)

    # segments are the mfcc like features
    full_array = hdf5.get_segments_pitches(h5)[:100]
    # flat array for features
    # only testing first 100 segments of any given song
    first_100_slice = np.zeros((minSegments, 12))
    first_100_slice[:full_array.shape[0], :full_array.shape[1]] = full_array
    feature = np.resize(first_100_slice, minSegments * 12) 
    feature_list.append(feature)

    h5.close()

def print_song_name(filename):
    h5 = hdf5.open_h5_file_read(filename)
    print hdf5.get_title(h5)
    h5.close()

def get_min_segments(filename):
    h5 = hdf5.open_h5_file_read(filename)
    shape = hdf5.get_segments_loudness_max(h5).shape[0]        
    if shape < minimum[0]:
        minimum[0] = shape
        print minimum[0]
    h5.close()

# this tries using loudness, tempo and time_sig
def feature_set_one(filename):
    fin = hdf5.open_h5_file_read(filename)
    features = []
    features.append(hdf5.get_time_signature(fin))
    features.append(hdf5.get_loudness(fin))
    features.append(hdf5.get_tempo(fin))
    feature_list.append(features)
    fin.close()

# gets the average 20 segments across the whole song
def feature_set_two(filename):
    fin = hdf5.open_h5_file_read(filename)
    
    # using these first
    features.append(hdf5.get_time_signature(fin))
    features.append(hdf5.get_loudness(fin))
    features.append(hdf5.get_tempo(fin))

    # going to get the 20 averages of loudness, chroma, and timbre
    fin.close()

# n1 will be the new shape of the array
def reduce_segments(segments, n1):
    if len(segments.shape) == 1:
        reduce_segments = np.zeros(n1)
    elif len(segments.shape) == 2:
        reduce_segments = np.zeros((n1, segments.shape[1])
    else:
        print "Unable to handle 3d feature sets"
        sys.exit(1)
    

def average_2d(arr):
    result = np.zeros(arr.shape[1])
    for i in xrange(arr.shape[1]):
        for arr_i in xrange(arr.shape[0]):
            result[i] += arr[i][arr_i]
    result = [x/float(arr.shape[0]) for x in result]
    return result

def average(arr):
    return sum(arr) / float(len(arr))

def extract_targets(filename):
    h5 = hdf5.open_h5_file_read(filename)

    # getting the target classes for the stuff
    # only 12 terms
    # for now we'll just use the first one
    terms = hdf5.get_artist_terms(h5)
    feature_list.append(terms)

    h5.close()

def extract_mb_terms(filename):
    h5 = hdf5.open_h5_file_read(filename)
    terms = hdf5.get_artist_mbtags(h5)
    #term_count = hdf5.get_artist_mbtags_count(h5)
    #feature_list.append((terms, term_count))
    feature_list.append(terms)
    h5.close()

def extract_timbre_pitches(filename):
    h5 = hdf5.open_h5_file_read(filename)
    segs = hdf5.get_segments_pitches(h5)[:minSegments]
    timbre = hdf5.get_segments_timbre(h5)[:minSegments]
    # to add the zero buffers
    first_n_timbre = np.zeros((minSegments, 12))
    first_n_timbre[:timbre.shape[0], :timbre.shape[1]] = timbre
    first_n_segs = np.zeros((minSegments, 12))
    first_n_segs[:segs.shape[0], :segs.shape[1]] = segs

    # flatenning
    segs_features = np.resize(first_n_segs, minSegments * 12)
    timbre_features = np.resize(first_n_timbre, minSegments * 12)
    feature = np.zeros(minSegments * 12 * 2)
    feature[:segs_features.shape[0]] = segs_features
    feature[segs_features.shape[0]:] = timbre_features
    feature_list.append(feature)
    h5.close()

def extract_timbre(filename):
    h5 = hdf5.open_h5_file_read(filename)
    timbre = hdf5.get_segments_timbre(h5)[:minSegments]
    first_100_slice = np.zeros((minSegments, 12))
    first_100_slice[:timbre.shape[0], :timbre.shape[1]] = timbre
    feature = np.resize(first_100_slice, minSegments * 12) 
    feature_list.append(feature)
    h5.close()

def extract_loudness(filename):
    h5 = hdf5.open_h5_file_read(filename)
    timbre = hdf5.get_segments_loudness_max(h5)[:minSegments]
    first_100_slice = np.zeros(minSegments)
    first_100_slice[:timbre.shape[0]] = timbre
    feature = np.resize(first_100_slice, minSegments) 
    feature_list.append(feature)
    h5.close()

def save_features(feats, path="feature_data.npy"):
    np.save(path, feats)

def load_array(filename="feature_data.npy"):
    return np.load(filename)

def extract():
    # if these are truly not here, create them
    if not os.path.exists("feature_data.npy"):
        print "Creating features file"
        apply_to_all_files(paths.msd_subset_data_path, func=extract_features)
        features = np.array(feature_list)
        save_features(features)
        clear_wrapper()

    if not os.path.exists("targets.npy"):
        print "Creating targets file"
        apply_to_all_files(paths.msd_subset_data_path, func=extract_targets)
        targets = np.array(feature_list)
        save_features(targets, "targets.npy")
        clear_wrapper()

def create_save_features(filename, func=lambda x:x):
    if not os.path.exists(filename):
        print "Creating {0} features".format(filename)
        apply_to_all_files(paths.msd_subset_data_path, func=func)
        targets = np.array(feature_list)
        save_features(targets, filename)
        clear_wrapper()

# creates a text file with the correct tags of the dataset
def set_correct_tag(array):
    index_map = {}
    tag_list = []
    with open("Genre_Targets.txt", "w") as tar:
        for i in xrange(len(array)):
            if len(array[i][0]) == 0:
                tar.write("Unknown\n")
            else:
                tag = get_tag(array[i])
                if len(tag) != 0:
                    tar.write("{}\n".format(tag))
                    tag_list.append(tag)
                    index_map[i] = len(tag_list) - 1
                else:
                    tar.write("Unknown\n")
    return index_map, tag_list

def get_tag(item):
    result = ""
    score = 0
    top_tags = ["classic pop and rock", "folk",
                "electronica", "jazz and blues",
                "soul and reggae", "punk",
                "metal", "classical", "pop", "hip hop"]

    tags = item[0]
    counts = item[1]
    for i in xrange(len(tags)):
        if tags[i] in top_tags:
            tag = tags[i]
            count = counts[i]
            if count >= score:
                result = tag
                score = count
    return result

def create_dataset(lst, dataset_name, extractor=lambda x:x):
    apply_to_all_listed_files(paths.msd_subset_data_path, lst, extractor)
    features_np = np.array(feature_list)
    save_features(features_np, dataset_name)
    clear_wrapper()


def main():
    if len(sys.argv) < 2:
        print "Needs some argument\n\
            To Generate Labels [labels]\n\
            To Generate Dataset [generate] [featureset] [fout] [fout]"
        sys.exit(1)
    if sys.argv[1] == "labels":
        print "Generating Track Ids and Labels"
        apply_to_all_files(paths.msd_subset_data_path, func=get_labels)
        save_list_to_text(feature_list, "TrackIds_Labels.txt")
        sys.exit(0)
    if sys.argv[1] == "generate":
        if not (os.path.isfile("test_labels.txt")
            and os.path.isfile("train_labels.txt")):
            print "please generate labels first"
            sys.exit(1)
        if len(sys.argv) < 5:
            print "Please choose feature set to generate"
            print "Please enter two file names [test] [train]"
            sys.exit(1)
        
        if sys.argv[2] == "1":
            func = feature_set_one
        test_labels = load_labels_text("test_labels.txt")
        train_labels = load_labels_text("train_labels.txt")
        create_dataset(test_labels, sys.argv[3], func)
        create_dataset(train_labels, sys.argv[4], func)
        sys.exit(0)

# this will be a mix of segments and beats?
if __name__=="__main__":
    main()