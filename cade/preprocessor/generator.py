import re
import os
import typing
import argparse
from pathlib import Path as pth
from extractor import CredentialExtractor

class Generator:
    """
    Generates Extracted Embedded Credentials.
    """
    def __init__(self, meta_path: str = None, cred_path: str = None) -> None:
        self.ce_light = CredentialExtractor()
        self.location = pth.cwd().parents[1] / "datasets/creddata/credentials"
        self.data_paths = pth.cwd().parents[1] / "datasets/creddata/meta", pth.cwd().parents[1] / "datasets/creddata/data"
        self.data_dirs = sorted(os.listdir(self.data_paths[0]), reverse = True), sorted(os.listdir(self.data_paths[1]), reverse = True)

    def binary_clstask(self) -> typing.Text:
        meta_path, cred_path = self.data_paths
        meta_dirs, cred_dirs = self.data_dirs 
        for meta_dir, cred_dir in zip(meta_dirs, cred_dirs):
            extractor = CredentialExtractor(meta_path / meta_dir, cred_path / cred_dir)
            positive = extractor.extract(
                extractor.groundtruth_bin(extractor.config.positive)
            )
            negative = extractor.extract(
                extractor.groundtruth_bin(extractor.config.negative)
            )
            extractor.utils.write_to_file(
                self.location / extractor.config.credentials, positive
            )
            extractor.utils.write_to_file(
                self.location / extractor.config.non_credentials, negative
            )
            
    def multivariate_clstask(self) -> typing.Text:
        meta_path, cred_path = self.data_paths
        meta_dirs, cred_dirs = self.data_dirs
        for filename, category in zip(self.ce_light.config.category.keys(), self.ce_light.config.category.values()):
            for meta_dir, cred_dir in zip(meta_dirs, cred_dirs):
                extractor = CredentialExtractor(meta_path / meta_dir, cred_path / cred_dir)
                ex_cat = extractor.extract(
                    extractor.groundtruth_mult(extractor.config.positive, category)
                )
                extractor.utils.write_to_file(
                    self.location / f"{filename}.txt", ex_cat
                )

    def _get_mct(self):
        return (
            self.ce_light.utils.process_message("Generating credentials for MCT..."),
            self.multivariate_clstask(), 
            self.ce_light.utils.process_message("Generation Complete!")
        )

    def _get_bct(self): 
        return (
            self.ce_light.utils.process_message("Generating credentials for BCT..."),
            self.binary_clstask(), 
            self.ce_light.utils.process_message("Generation Complete!")
        )

    def _get_mct_bct(self):
        return (
            self.ce_light.utils.process_message("Generating credentials for MCT & BCT..."),
            self._get_mct(),
            self._get_bct(),
            self.ce_light.utils.process_message("Generation Complete!")
        )

if __name__ == "__main__":
    gen = Generator()
    parser = argparse.ArgumentParser(description = "Generates Observations for Multivariate & Binary Classification Tasks")
    parser.add_argument("--task", type = str, help = "Enter classification (mct or bct) task")
    args = parser.parse_args()
    if re.match(args.task, "mct",  re.IGNORECASE): 
        gen._get_mct()
    elif re.match(args.task, "bct", re.IGNORECASE): 
        gen._get_bct()
    elif re.match(args.task, "mbct", re.IGNORECASE): 
        gen._get_mct_bct()