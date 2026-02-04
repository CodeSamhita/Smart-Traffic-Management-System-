#this code is used for downloading the data set.
import kagglehub

# Download selected version
path = kagglehub.dataset_download("dataclusterlabs/indian-vehicle-dataset/versions/1")

print("Path to dataset files:", path)