import sys
sys.path.append(".")
import os
import typing
from CADE.utils import Utils as ut
from extractor import CredentialExtractor

def binary_clstask():
    pass

def multivariabe_clstask():
    pass

if __name__ == "__main__":
    root_dir = f"{os.getcwd()}/datasets/creddata/"
    groundtruth = ut.config()["groundtruth"]
    negative, positive = groundtruth["negative"], groundtruth["positive"]

    meta_path = root_dir + "meta/"
    meta_dirs = sorted(os.listdir(meta_path), reverse = True)
    cred_path = root_dir + "data/"
    cred_dirs = sorted(os.listdir(cred_path), reverse = True)

    for meta_dir, cred_dir in zip(meta_dirs, cred_dirs):
        location = root_dir + "credentials/"
        CE = CredentialExtractor(meta_path + meta_dir, cred_path + cred_dir)
        CE.write(location + list(category.keys())[2] + ".txt", CE.groundtruth([positive], category["private_key"]))
