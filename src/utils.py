from __future__ import with_statement

import re
import os
import json
import pickle
from typing import Dict, Sequence, List, Set, Text, Union

class Utils:
	@classmethod
	def __len__(self, arg: Union[Sequence, Text, Dict, Set]) -> int:
		if (isinstance(arg, (int, float, bool))):
			raise TypeError("Invalid argument. Only text, sequence, mapping and set are accepted")
		else: return len(arg)

	@classmethod
	def cleaner(self, data: List[str]) -> List[str]:
		out = []
		[out.append(re.sub(r"[^\w\s]", "", obs.strip())) for obs in data]
		return out
	
	@classmethod
	def pickle(self, data: List[Union[str, float]], file_name: str):
		with open(file_name, "wb") as file:
			pickle.dump(data, file)
	
	@classmethod
	def unpickle(self, data: List[Union[str, float]]) -> Union[List[str], List[float]]:
		with open(data, "rb") as file:
			loaded = pickle.load(file)
		return loaded
	
	@classmethod
	def reader(self, root: str, file: str) -> List:
		with open(os.path.join(root, file), "r") as f:
			return f.readlines()
	
	@classmethod
	def config(self, path: str = "configs/config.json"):
		with open(path, "r") as f:
			return json.load(f)