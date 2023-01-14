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
		try:
			with open(file_name, "wb") as file:
				pickle.dump(data, file)
		except FileNotFoundError as e:
			raise(e)
	
	@classmethod
	def unpickle(self, data: List[Union[str, float]]) -> Union[List[str], List[float]]:
		try:
			with open(data, "rb") as file:
				return pickle.load(file)
		except FileNotFoundError as e:
			raise(e)
	
	@classmethod
	def reader(self, root: str, file: str) -> List:
		try:
			with open(os.path.join(root, file), "r") as f:
				return f.readlines()
		except FileNotFoundError as e:
			raise(e)
	
	@classmethod
	def config(self, path: List[str] = ["configs/default.json", "configs/ml.json"]):
		try:
			with open(path[0], "r") as default, open(path[1], "r") as ml:
				return json.load(default), json.load(ml)
		except FileNotFoundError as e:
			raise(e)
			