from __future__ import with_statement
import sys
sys.path.append(".")
import os
import pandas
import typing
from CADE.config import Config
from CADE.utils import Utils as ut

class CredentialExtractor:
    def __init__(self, meta_path: str = None, secrets_path: str = None) -> None:
        self.meta_path = meta_path
        self.secrets_path = secrets_path
        self.config = Config()
    
    def metadata(self) -> pandas.DataFrame:
        try:
            meta: pandas.DataFrame = pandas.read_csv(self.meta_path)
        except FileNotFoundError as e:
            raise(e)
        meta[self.config.fp] = meta[self.config.fp].apply(lambda fp: fp.split("/")[-1]) 
        meta[self.config.lsle] = meta[self.config.lsle].apply(lambda x: x.split(":")[0])
        return meta
    
    def groundtruth(self, groundtruth: typing.List[str], category: typing.List[str] = [None]) -> typing.Tuple[typing.List]: 
        meta = self.metadata().loc[(self.metadata()[self.config.gt].isin(groundtruth)) & (self.metadata()[self.config.cat].isin(category))]
        return [fp for fp in meta[self.config.fp]], [int(lidx) for lidx in meta[self.config.lsle]]

    def extract(self, data: typing.List[str]) -> typing.Set[str]:
        temp, out = {}, []
        filepath, lineidx = data
        for fp, lidx in zip(filepath, lineidx):
            if fp in temp:
                temp[fp].append(lidx - 1)
            else: 
                temp[fp] = [lidx - 1]
        for root, _, files in os.walk(self.secrets_path):
            for file in files:
                if file in temp:
                    vals = temp[file]
                    if ut.__len__(vals) == 1:
                        instance = ut.reader(root, file)[vals[0]]
                        out.append(instance[:-1].strip())
                    else:
                        for idx in vals:
                            instance = ut.reader(root, file)[idx]
                            out.append(instance[:-1].strip())
        return set(out)

    def write(self, path: str, data: typing.List[str]):
        operator = "a" if os.path.exists(path) else "w"
        with open(path, operator) as f:
            f.write("\n".join(self.extract(data)) + "\n")