from __future__ import with_statement, print_function

import re
import os
import json
import pickle
import typing

class Utils:
	"""
	This module is reponsible for providing helper methods
	"""
	@classmethod
	def __len__(self, arg: typing.Union[typing.Sequence, typing.Text, typing.Dict, typing.Set]) -> int:
		if (isinstance(arg, (int, float, bool))):
			raise TypeError("Invalid argument. Only text, sequence, mapping and set are accepted")
		else: 
			return len(arg)

	@classmethod
	def cleaner(self, data: typing.List[str]) -> typing.List[str]:
		return [re.sub(r"[^\w\s]", "", obs.strip()) for obs in data]
	
	@classmethod
	def pickle(self, data: typing.List[typing.Union[str, float]], file_name: str):
		try:
			with open(file_name, "wb") as file:
				pickle.dump(data, file)
		except FileNotFoundError as e:
			raise(e)
	
	@classmethod
	def unpickle(self, data: typing.List[typing.Union[str, float]]) -> typing.Union[typing.List[str], typing.List[float]]:
		try:
			with open(data, "rb") as file:
				return pickle.load(file)
		except FileNotFoundError as e:
			raise(e)
	
	@classmethod
	def reader(self, root: str, file: str) -> typing.List:
		try:
			with open(os.path.join(root, file), "r") as f:
				return f.readlines()
		except FileNotFoundError as e:
			raise(e)
	
	@classmethod
	def config(self, path: typing.List[str]):
		try:
			with open(path[0], "r") as default, open(path[1], "r") as ml:
				return json.load(default), json.load(ml)
		except FileNotFoundError as e:
			raise(e)
	
	@classmethod
	def process_message(self, msg: str):
		print("Process:::"+ msg)