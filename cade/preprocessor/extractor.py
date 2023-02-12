import os
import pandas
import typing
import importlib as im
from pathlib import Path

class CredentialExtractor:
	"""
	Extracts Embedded Credential Observations.
	Arg: Path to Embedded Credential & Corresponding Metadata Directories
	"""
	def __init__(self, meta_path: str = None, cred_path: str = None) -> None:
		self.im_mod = im.util.spec_from_file_location("primps", Path.cwd().parents[0]/"primps.py")
		self.meta_path, self.cred_path  = meta_path, cred_path
		self.utils, self.config = self.im_mod.loader.load_module().import_helper_modules()
	
	def metadata(self) -> pandas.DataFrame:
		try:
			meta: pandas.DataFrame = pandas.read_csv(self.meta_path)
		except FileNotFoundError as e:
			raise(e)
		meta[self.config.fp] = meta[self.config.fp].apply(lambda fp: fp.split("/")[-1]) 
		meta[self.config.lsle] = meta[self.config.lsle].apply(lambda x: x.split(":")[0])
		return meta

	def groundtruth_bin(self, groundtruth: typing.List[str]) -> typing.Tuple[typing.List]:
		meta = self.metadata().loc[self.metadata()[self.config.gt].isin(groundtruth)] 
		return [fp for fp in meta[self.config.fp]], [int(lidx) for lidx in meta[self.config.lsle]]

	def groundtruth_mult(self, groundtruth: typing.List[str], category: typing.List[str]) -> typing.Tuple[typing.List]: 
		meta = self.metadata().loc[self.metadata()[self.config.gt].isin(groundtruth)]
		meta = self.metadata().loc[self.metadata()[self.config.cat].isin(category)]
		return [fp for fp in meta[self.config.fp]], [int(lidx) for lidx in meta[self.config.lsle]]

	def groundtruth(self, groundtruth: typing.List[str], category: typing.List[str]) -> typing.Tuple[typing.List]: 
		meta = self.metadata().loc[(self.metadata()[self.config.gt].isin(groundtruth)) & (self.metadata()[self.config.cat].isin(category))]
		return [fp for fp in meta[self.config.fp]], [int(lidx) for lidx in meta[self.config.lsle]]

	def extract(self, data: typing.List[str]) -> typing.Set[str]:
		temp: typing.Dict = {} 
		out: typing.List = []
		filepath, lineidx = data
		for fp, lidx in zip(filepath, lineidx):
			if fp in temp:
				temp[fp].append(lidx - 1)
			else: 
				temp[fp] = [lidx - 1]
		for root, _, files in os.walk(self.cred_path):
			for file in files:
				if file in temp:
					vals = temp[file]
					if self.utils.__len__(vals) == 1:
						instance = self.utils.reader(root, file)[vals[0]]
						out.append(instance[:-1].strip())
					else:
						for idx in vals:
							instance = self.utils.reader(root, file)[idx]
							out.append(instance[:-1].strip())
		return set(list(out))

	def write(self, path: str, data: typing.List[str]): 
		operator = "a" if os.path.exists(path) else "w"
		with open(path, operator) as f:
			f.write("\n".join(self.extract(data)) + "\n" )