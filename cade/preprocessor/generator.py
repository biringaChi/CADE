import re
import os
import typing
import argparse
import importlib as im
from pathlib import Path as pth

# ZIP CRED DIRECTORY

class Generator:
    """
    Generates Extracted Embedded Credentials.
    Args: 
    """
    def __init__(self) -> None:
        self.root_dir: str = pth.cwd().parents[1] / "creddata"
        self.cred_pth: str = self.root_dir / "data"
        self.meta_pth: str = self.root_dir / "meta"
        self.location = self.root_dir / "credentials"
        self.meta_dirs = sorted(os.listdir(self.meta_pth), reverse = True)
        self.cred_dirs = sorted(os.listdir(self.cred_pth), reverse = True)
        self.extractor = im.import_module("extractor")
        self.config = im.util.spec_from_file_location("config", self.file_pth / "config.py").loader.load_module()

    def binary_clstask(self) -> typing.Text:
        for meta_dir, cred_dir in zip(self.meta_dirs, self.cred_dirs):
            extract_observations = self.extractor.ObservationExtractor(self.meta_path + meta_dir, self.cred_path + cred_dir)
            extract_observations.write(self.location + self.config.Config().credentials + ".txt", extract_observations.groundtruth_bin(self.config.Config().positive))
            extract_observations.write(self.location + self.config.Config().non_credentials + ".txt", extract_observations.groundtruth_bin(self.config.Config().negative))

    def multivariate_clstask(self) -> typing.Text:
        for filename, category in zip(self.config.category.keys(), self.config.category.values()):
            for meta_dir, cred_dir in zip(self.meta_dirs, self.cred_dirs):
                extract_observations = self.extractor.ObservationExtractor(self.meta_path + meta_dir, self.cred_path + cred_dir)
                extract_observations.write(self.location + filename + ".txt", extract_observations.groundtruth_mult(self.config.positive, category))
    
#     def get_bin(self): 
#         return (
#             ut.process_message("Generating BIN Credentials..."),
#                 self.binary_clstask(), 
#             ut.process_message("BIN Generation Complete!")
#         )
    
#     def get_mult(self):
#         return (
#             ut.process_message("Generating MULT Credentials..."),
#                 self.multivariate_clstask(), 
#             ut.process_message("MULT Generation Complete!")
#         )

#     def get_default(self):
#         return (
#             ut.process_message("Generating BIN & MULT Credentials..."),
#                 self.get_bin(),
#                 self.get_mult(),
#             ut.process_message("BIN & MULT Generation Complete!")
#         )

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description = "Generates Embedded Credentials' Observations for Binary & Multivariate Classification Tasks")
#     parser.add_argument("task", type = str, help = "Enter classification (bin or mult) task")
#     args = parser.parse_args()
#     gen = Generator()
#     if re.match(args.task, "bin", re.IGNORECASE): 
#         gen.get_bin()
#     elif re.match(args.task, "mult", re.IGNORECASE): 
#         gen.get_mult() 
#     else: 
#         gen.get_default()


Generator()