import re
import os
import typing
import argparse
from pathlib import Path
from extractor import CredentialExtractor

class Generator(CredentialExtractor):
    """
    Generates Extracted Embedded Credentials.
    """
    def __init__(self, meta_path: str = None, cred_path: str = None) -> None:
        super().__init__(meta_path, cred_path)
        self.location = Path.cwd().parents[1] / "datasets/creddata/credentials"
        self.data_paths = Path.cwd().parents[1] / "datasets/creddata/meta", Path.cwd().parents[1] / "datasets/creddata/data"
        self.data_dirs = sorted(os.listdir(self.data_paths[0]), reverse = True), sorted(os.listdir(self.data_paths[1]), reverse = True)

    def binary_clstask(self) -> typing.Text:
        meta_path, cred_path = self.data_paths
        meta_dirs, cred_dirs = self.data_dirs 
        for meta_dir, cred_dir in zip(meta_dirs, cred_dirs):
            CE = CredentialExtractor(meta_path / meta_dir, cred_path / cred_dir)
            CE.write(
                self.location / self.config.credentials, 
                CE.groundtruth_bin(self.config.positive)
                )
            CE.write(
                self.location / self.config.non_credentials, 
                CE.groundtruth_bin(self.config.negative)
                )

    def multivariate_clstask(self) -> typing.Text:
        meta_path, cred_path = self.data_paths
        meta_dirs, cred_dirs = self.data_dirs 
        for filename, category in zip(self.config.category.keys(), self.config.category.values()):
            for meta_dir, cred_dir in zip(meta_dirs, cred_dirs):
                CE = CredentialExtractor(meta_path / meta_dir, cred_path / cred_dir)
                CE.write(
                    self.location / f"{filename}.txt",
                    CE.groundtruth_mult(self.config.positive, category)
                    )

    def _get_mct(self):
        return (
            self.utils.process_message("Generating credentials for MCT..."),
            self.multivariate_clstask(), 
            self.utils.process_message("Generation Complete!")
        )

    def _get_bct(self): 
        return (
            self.utils.process_message("Generating credentials for BCT..."),
            self.binary_clstask(), 
            self.utils.process_message("Generation Complete!")
        )

    def _get_mct_bct(self):
        return (
            self.utils.process_message("Generating credentials for MCT & BCT..."),
            self._get_mct(),
            self._get_bct(),
            self.utils.process_message("Generation Complete!")
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
        