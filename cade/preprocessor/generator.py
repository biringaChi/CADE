import argparse
import os
import typing
import re

# from code.conf import Config
# from code.utils import Utils as ut
# from extractor import CredentialExtractor

class Generator:
    """
    Generates Extracted Embedded Credentials.
    """
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
            CE.write(self.location + self.config.credentials + ".txt", CE.groundtruth_bin(self.config.positive))
            CE.write(self.location + self.config.non_credentials + ".txt", CE.groundtruth_bin(self.config.negative))

    def multivariate_clstask(self) -> typing.Text:
        for filename, category in zip(self.config.category.keys(), self.config.category.values()):
            for meta_dir, cred_dir in zip(self.meta_dirs, self.cred_dirs):
                CE = CredentialExtractor(self.meta_path + meta_dir, self.cred_path + cred_dir)
                CE.write(self.location + filename + ".txt", CE.groundtruth_mult(self.config.positive, category))
    
    def get_bin(self): 
        return (
            ut.process_message("Generating BIN Credentials..."),
                self.binary_clstask(), 
            ut.process_message("BIN Generation Complete!")
        )
    
    def get_mult(self):
        return (
            ut.process_message("Generating MULT Credentials..."),
                self.multivariate_clstask(), 
            ut.process_message("MULT Generation Complete!")
        )

    def get_default(self):
        return (
            ut.process_message("Generating BIN & MULT Credentials..."),
                self.get_bin(),
                self.get_mult(),
            ut.process_message("BIN & MULT Generation Complete!")
        )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "Generates Embedded Credentials' Observations for Binary & Multivariate Classification Tasks")
    parser.add_argument("task", type = str, help = "Enter classification (bin or mult) task")
    args = parser.parse_args()
    gen = Generator()
    if re.match(args.task, "bin", re.IGNORECASE): 
        gen.get_bin()
    elif re.match(args.task, "mult", re.IGNORECASE): 
        gen.get_mult() 
    else: 
        gen.get_default()
