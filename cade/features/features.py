from __future__ import division, annotations

import importlib as im
from pathlib import Path
from simpletransformers.language_representation import RepresentationModel


class Features:
	def __init__(self) -> None:
		self.im_mod = im.util.spec_from_file_location("primps", Path.cwd().parents[0]/"primps.py")
		self.utils, self.config = self.im_mod.loader.load_module().import_helper_modules()

	def retrieve_observations(self):
		pass

	def fine_tune(self, data, combine_strategy, batch_size):
		repr_model = RepresentationModel(
			model_type = "bert",
			model_name = "bert-base-uncased",
			use_cuda = False
		)
		return repr_model().encode_sentences(data, combine_strategy, batch_size)
	
	def retrieve_features(self):
		pass 