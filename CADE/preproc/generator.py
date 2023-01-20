import argparse
import sys
sys.path.append(".")
import os
import typing
import pandas as pd
from CADE.config import Config
from CADE.utils import Utils as ut
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
        for meta_dir, cred_dir in zip(self.meta_dirs, self.cred_dirs):
            CE = CredentialExtractor(self.meta_path + meta_dir, self.cred_path + cred_dir)
            category = [cat[0] for cat in self.config.category.values()]
            CE.write(self.location + "positive.txt", CE.groundtruth(self.config.positive, category))
            CE.write(self.location + "neg.txt", CE.neg(self.config.negative))

    def multiclass_clstask(self) -> typing.Text:
        for filename, category in zip(self.config.category.keys(), self.config.category.values()):
            for meta_dir, cred_dir in zip(self.meta_dirs, self.cred_dirs):
                CE = CredentialExtractor(self.meta_path + meta_dir, self.cred_path + cred_dir)
                CE.write(self.location + filename + ".txt", CE.groundtruth(self.config.positive, category))
    
    def call_bin(self): 
        return (ut.process_message("Generating Credentials..."), 
                self.binary_clstask(), 
                ut.process_message("Generation Complete!")
        )
    
    def call_mult(self):
        pass

    def default(self):
        return (self.call_bin(),
                self.call_mult(),
        )

if __name__ == "__main__":
    Generator().call_bin()