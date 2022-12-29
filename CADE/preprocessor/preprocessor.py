from __future__ import with_statement

import os
import pandas as pd
from utils import Utils as ut
from typing import List, Set, Tuple

class CredDataMiner:
	def __init__(self, meta_path: str = None, secrets_path: str = None) -> None:
		self.meta_path = meta_path
		self.secrets_path = secrets_path
		self.ut = ut.config()["metacols"]
		self.fp, self.lsle, self.gt = self.ut["fp"], self.ut["lsle"], self.ut["gt"]
	
	def meta_data(self) ->  pd.DataFrame:
		meta: pd.DataFrame = pd.read_csv(self.meta_path)
		meta[self.fp] = meta[self.fp].apply(lambda fp: fp.split("/")[-1])
		meta[self.lsle] = meta[self.lsle].apply(lambda x: x.split(":")[0])
		return meta
	
	def groundtruth(self, filter: List[str]) -> Tuple[list]: 
		meta = self.meta_data().loc[self.meta_data()[self.gt].isin(filter)]
		return [fp for fp in meta[self.fp]], [int(lidx) for lidx in meta[self.lsle]]

	def dig(self, data: List[str]) -> Set:
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

	def write(self, path: str, data: List[str]):
		operator = "a" if os.path.exists(path) else "w"
		with open(path, operator) as f:
			f.write("\n".join(self.dig(data)) + "\n")

if __name__ == "__main__":
	negative_class = ut.config()["groundtruth"]["negative"]
	positive_class = ut.config()["groundtruth"]["positive"]
	# partial_positive_class = ut.config()["groundtruth"]["partial_positive"]

	meta_path = f"{os.getcwd()}/repositories/meta/"
	meta_dirs = sorted(os.listdir(meta_path), reverse = True)

	cred_path = f"{os.getcwd()}/repositories/data/"  
	cred_dirs = sorted(os.listdir(cred_path), reverse = True)

	for meta_dir, cred_dir in zip(meta_dirs, cred_dirs):
		location = f"{os.getcwd()}/datasets/"
		if os.path.exists(location): 
			raise ValueError(f"Data already exist in this location: {location}")
		else:
			rm = CredDataMiner(meta_path + meta_dir, cred_path + cred_dir)
			rm.write(location + ut.config()["metacols"]["bn"], rm.groundtruth([negative_class]))
			rm.write(location + ut.config()["metacols"]["sn"], rm.groundtruth([positive_class]))


class LinkedInMiner:
	pass