# this should be imported by all the other modules
import os
import sys

project_path = os.path.abspath("../")
msd_subset_path = os.path.join(project_path, "MillionSongSubset")
msd_subset_data_path = os.path.join(msd_subset_path, "data")
msd_subset_addf_path = os.path.join(msd_subset_path, "AdditionalFiles")
assert os.path.isdir(msd_subset_path), "No Path"

# adding the hdf5 code to the project
msd_code_path = os.path.join(project_path, "MSongsDB/PythonSrc")
sys.path.append(msd_code_path)