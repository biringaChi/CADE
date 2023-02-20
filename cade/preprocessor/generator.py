import re
import typing
import argparse
from extractor import CredentialExtractor

parser = argparse.ArgumentParser(description = "Generates Observations for Multivariate & Binary Classification Tasks")
parser.add_argument(
    "-t",
    "--task", 
    type = str, 
    metavar = "",
    required = True,
    help = "Enter classification (mct or bct) task"
    )
args = parser.parse_args()

class Generator:
    """
    Generates Extracted Embedded Credentials.
    Arg: Classification Task
    """
    def __init__(self, meta_path: str = None, cred_path: str = None) -> None:
        self.ce = CredentialExtractor()
        self.navigator = self.ce.utils.navigator()
        self.location = self.navigator["credentials"]
        self.meta_path, self.cred_path = self.navigator["meta_path"], self.navigator["cred_path"]
        self.meta_dirs, self.cred_dirs = self.navigator["meta_dirs"], self.navigator["cred_dirs"]

    def binary_clstask(self) -> typing.Text:
        for meta_dir, cred_dir in zip(self.meta_dirs, self.cred_dirs):
            extractor = CredentialExtractor(self.meta_path / meta_dir, self.cred_path / cred_dir)
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
        for filename, category in zip(self.ce.config.category.keys(), self.ce.config.category.values()):
            for meta_dir, cred_dir in zip(self.meta_dirs, self.cred_dirs):
                extractor = CredentialExtractor(self.meta_path / meta_dir, self.cred_path / cred_dir)
                ex_cat = extractor.extract(
                    extractor.groundtruth_mult(extractor.config.positive, category)
                )
                extractor.utils.write_to_file(
                    self.location / f"{filename}.txt", ex_cat
                )
                
    def _get_mct(self):
        return (
            self.ce.logger._info("Generating credentials for MCT..."),
            self.multivariate_clstask(), 
            self.ce.logger._info("Generation Complete!")
        )

    def _get_bct(self): 
        return (
            self.ce.logger._info("Generating credentials for BCT..."),
            self.binary_clstask(), 
            self.ce.logger._info("Generation Complete!")
        )

    def _get_mct_bct(self):
        return (
            self.ce.logger._info("Generating credentials for MCT & BCT..."),
            self._get_mct(),
            self._get_bct(),
            self.ce.logger._info("Generation Complete!")
        )

if __name__ == "__main__":
    gen = Generator()
    if re.match(args.task, "mct",  re.IGNORECASE): 
        gen._get_mct()
    elif re.match(args.task, "bct", re.IGNORECASE): 
        gen._get_bct()
    elif re.match(args.task, "mbct", re.IGNORECASE): 
        gen._get_mct_bct()