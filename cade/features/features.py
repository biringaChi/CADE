from __future__ import division, annotations

import importlib as im
from pathlib import Path
from simpletransformers.config.model_args import ModelArgs
from simpletransformers.language_representation import RepresentationModel

class FeatureExtraction:
	def __init__(self) -> None:
		self.im_mod = im.util.spec_from_file_location("primps", Path.cwd().parents[0]/"primps.py")
		self.utils, self.config = self.im_mod.loader.load_module().import_helper_modules()
	
	def __getitem__():
		# TODO
		pass 

	def fine_tune(self, model_type: str, model_name: str, length: int):
		return RepresentationModel(
			model_type = model_type, model_name = model_name,
			args = ModelArgs(max_seq_length = length), use_cuda = False
		)

	def model(self, data, combine_strategy, batch_size, model_type, model_name, length):
		return self.fine_tune(model_type, model_name, length).encode_sentences(data, combine_strategy, batch_size)