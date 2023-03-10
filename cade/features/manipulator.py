import numpy
import typing
import importlib
from pathlib import Path as p

class Manipulator:
	"""
	Handles Generated Contextual Feature Embeddings 
	"""
	def __init__(self) -> None:
		super().__init__()
		self.helper = importlib.util.spec_from_file_location("primps", p.cwd().parents[0]/"primps.py")
		self.utils, self.config, self.logger = self.helper.loader.load_module().import_helper_modules()

	def truncation(self, features):
		truncated_features = []
		if features.shape[self.config.one] > self.config.max_seqlen:
			for feature in features:
				truncated_features.append(feature[:self.config.max_seqlen])
			return numpy.asarray(truncated_features)
		return features
	
	def truncation_m(self, *features):
		return [self.truncation(feature) for feature in features]
	
	def padding(self, features):
		pass

	def padding_m(self, *features):
		pass

	def transform(self, features):
		pass

	def _pipeline(self, features):
		pass
