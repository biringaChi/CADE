import os
import pandas
import typing
import importlib as im
from pathlib import Path as pth

class ObservationExtractor:
	"""
	Extracts Embedded Credential Observations.
	Args: 
		Embedded Credential Directory.
		Corresponding Metadata Directory.
	"""
	def __init__(self, meta_path: str = None, secrets_path: str = None) -> None:
		self.meta_path = meta_path
		self.secrets_path = secrets_path
		self.file_pth: str = pth.cwd().parents[0] / "helper"
		self.utils = im.util.spec_from_file_location("utils", self.file_pth / "utils.py").loader.load_module()
		self.config = im.util.spec_from_file_location("config", self.file_pth / "config.py").loader.load_module()
		
	def __str__(self) -> str:
		return self.__class__.__name__

	def __repr__(self) -> str:
		return self.__str__()
	
	def metadata(self) -> pandas.DataFrame:
		try:
			meta: pandas.DataFrame = pandas.read_csv(self.meta_path)
		except FileNotFoundError as e:
			raise(e)
		meta[self.config.Config().fp] = meta[self.config.Config().fp].apply(lambda fp: fp.split("/")[-1]) 
		meta[self.config.Config().lsle] = meta[self.config.Config().lsle].apply(lambda x: x.split(":")[0])
		return meta

	def groundtruth_bin(self, groundtruth: typing.List[str]) -> typing.Tuple[typing.List]:
		meta = self.metadata().loc[self.metadata()[self.config.Config().gt].isin(groundtruth)] 
		return [fp for fp in meta[self.config.Config().fp]], [int(lidx) for lidx in meta[self.config.Config().lsle]]
		# return ([fp for fp in self.metadata().loc[self.metadata()[self.config.Config().gt].isin(groundtruth)][self.config.Config().fp]], 
		# 		[int(lidx) for lidx in self.metadata().loc[self.metadata()[self.config.Config().gt].isin(groundtruth)][self.config.Config().lsle]])

	def groundtruth_mult(self, groundtruth: typing.List[str], category: typing.List[str]) -> typing.Tuple[typing.List]: 
		meta = self.metadata().loc[self.metadata()[self.config.Config().gt].isin(groundtruth) & self.metadata()[self.config.Config().category].isin(category)]
		return [fp for fp in meta[self.config.Config().fp]], [int(lidx) for lidx in meta[self.config.Config().lsle]]

	def extract(self, data: typing.List[str]) -> typing.Set[str]:
		temp: typing.Dict = {}, 
		out: typing.List = []
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
					if self.utils.Utils.__len__(vals) == 1:
						instance = self.utils.Utils.reader(root, file)[vals[0]]
						out.append(instance[:-1].strip())
					else:
						for idx in vals:
							instance = self.utils.Utils.reader(root, file)[idx]
							out.append(instance[:-1].strip())
		return set(out)

	def write(self, path: str, data: typing.List[str]):
		operator = "a" if os.path.exists(path) else "w"
		with open(path, operator) as f:
			f.write("\n".join(self.extract(data)) + "\n") # change one n maybe?, fix though? or prep function to split