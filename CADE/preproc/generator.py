import sys
sys.path.append(".")
import argparse
import os
import typing
import re
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
    
    def binary_clstask(self) -> typing.Text:
        for meta_dir, cred_dir in zip(self.meta_dirs, self.cred_dirs):
            CE = CredentialExtractor(self.meta_path + meta_dir, self.cred_path + cred_dir)
            category = [cat[0] for cat in self.config.category.values()]
            CE.write(self.location + self.config.credentials + ".txt", CE.groundtruth(self.config.positive, category))
            CE.write(self.location + self.config.non_credentials + ".txt", CE.neg(self.config.negative))

    def multivariate_clstask(self) -> typing.Text:
        for filename, category in zip(self.config.category.keys(), self.config.category.values()):
            for meta_dir, cred_dir in zip(self.meta_dirs, self.cred_dirs):
                CE = CredentialExtractor(self.meta_path + meta_dir, self.cred_path + cred_dir)
                CE.write(self.location + filename + ".txt", CE.groundtruth(self.config.positive, category))
    
    def _call_bin(self): 
        return (
            ut.process_message("Generating BIN Credentials..."),
                self.binary_clstask(), 
            ut.process_message("BIN Generation Complete!")
        )
    
    def _call_mult(self):
        return (
            ut.process_message("Generating MULT Credentials..."),
                self.multivariate_clstask(), 
            ut.process_message("MULT Generation Complete!")
        )

    def _call_default(self):
        return (
            ut.process_message("Generating BIN & MULT Credentials..."),
                self._call_bin(),
                self._call_mult(),
            ut.process_message("BIN & MULT Generation Complete!")
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Generates Embedded Credentials' Observations for Binary & Multivariate Classification Task")
    gen = Generator()
    parser.add_argument("--task", type = str)
    args = parser.parse_args()
    if re.match(args.task, "bin", re.IGNORECASE): 
        gen._call_bin()
    elif re.match(args.task, "mult", re.IGNORECASE): 
        gen._call_mult()
    else: 
        gen._call_default()