from __future__ import division, annotations
from simpletransformers.language_representation import RepresentationModel


class Features:
	def __init__(self) -> None:
		pass

	def fine_tune(self, data, combine_strategy, batch_size):
		repr_model = RepresentationModel(
			model_type = "bert",
			model_name = "bert-base-uncased",
			use_cuda = False
		)
		return repr_model().encode_sentences(data, combine_strategy, batch_size)
	
	def get_features(self):
		pass