import argparse
import sys
sys.path.append(".")
import os
import typing
from CADE.config import Config
from CADE.utils import Utils
from extractor import CredentialExtractor

config = Config()
# ut = Utils()
# 
def binary_clstask():
    pass

def multiclass_clstask():
    for meta_dir, cred_dir in zip(meta_dirs, cred_dirs):
        location = root_dir + "testcred/"
        CE = CredentialExtractor(meta_path + meta_dir, cred_path + cred_dir)
        for filename, category in zip(config.category.keys(), config.category.values()):
            CE.write(location + filename + ".txt", CE.groundtruth(config.positive, category))

if __name__ == "__main__":
    root_dir = f"{os.getcwd()}/datasets/creddata/"

    meta_path = root_dir + "meta/"
    meta_dirs = sorted(os.listdir(meta_path), reverse = True)
    cred_path = root_dir + "data/"
    cred_dirs = sorted(os.listdir(cred_path), reverse = True)
    # process_message("Extracting Raw EC ")
    multiclass_clstask()
    # process_message()
