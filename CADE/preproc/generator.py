import argparse
import sys
sys.path.append(".")
import os
import typing
from CADE.config import Config
from CADE.utils import Utils
from extractor import CredentialExtractor

class Generator:
    def __init__(self) -> None:
        self.config = Config()
        self.root_dir = f"{os.getcwd()}/datasets/creddata/"
        self.location = self.root_dir + "credentials/"
        self.meta_path = self.root_dir + "meta/"
        self.meta_dirs = sorted(os.listdir(self.meta_path), reverse = True)
        self.cred_path = self.root_dir + "data/"
        self.cred_dirs = sorted(os.listdir(self.cred_path), reverse = True)
    
    def binary_clstask(self):
        # TODO
        pass

    def multiclass_clstask(self) -> typing.Text:
        for filename, category in zip(self.config.category.keys(), self.config.category.values()):
            for meta_dir, cred_dir in zip(self.meta_dirs, self.cred_dirs):
                CE = CredentialExtractor(self.meta_path + meta_dir, self.cred_path + cred_dir)
                CE.write(self.location + filename + ".txt", CE.groundtruth(self.config.positive, category))

if __name__ == "__main__":
    Utils.process_message("Generating Credentials...")
    Generator().multiclass_clstask()
    Utils.process_message("Generation Complete!")