#! /usr/bin/python
# this script should be used to split the features into a training
# and test set
# train is 0.8 while test is 0.2

import features

tracks_labels = features.load_labels_text("TrackIds_Labels.txt")
top_tags = ["classic pop and rock", "folk",
            "electronica", "jazz and blues",
            "soul and reggae", "punk",
            "metal", "classical", "pop", "hip hop"]

print "Total: {0}\nTest: {1}\n".format(len(tracks_labels), len(tracks_labels)/5)

tag_count = {}
max_test_set = {}
for tag in top_tags:
    tag_count[tag] = 0

# recounting the items
for track_id, label in tracks_labels:
    tag_count[label] += 1

# test set is 1/5 of my whole set
# resetting tag_count to be used for counting up to the max
for key in tag_count:
    max_test_set[key] = tag_count[key]/5
    print "{0}: {1}".format(key, max_test_set[key])
    tag_count[key] = 0

# Split the array into a test set and then a train set
# and then save it
train_set = []
test_set = []

for i in xrange(len(tracks_labels)):
    track, tag = tracks_labels[i]
    if tag_count[tag] < max_test_set[tag]:
        test_set.append(tracks_labels[i])
        tag_count[tag] += 1
    else:
        train_set.append(tracks_labels[i])

features.save_list_to_text(train_set, "train_labels.txt")
features.save_list_to_text(test_set, "test_labels.txt")