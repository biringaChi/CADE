import numpy
import typing
from features import ContextualEmbeddings

class Manipulator(ContextualEmbeddings):
	"""
	Handles Generated Contextual Feature Embeddings 
	"""
	def __init__(self) -> None:
		super().__init__()
	
	def verify_shape(self):
		pass
	
	def truncation(self, features):
		truncated_observations = []
		for feature in features:
			if feature > self.config.max_seqlen:
				truncated_observations.append(feature[:self.config.max_seqlen])
			else:
				truncated_observations.append(feature)
		return truncated_observations

	def padding(self, features):
		padded_observations  = []
		for feature in features:
			if self.utils.__len__(feature) < self.config.max_seqlen:
				feature.extend([0.0] * (self.config.max_seqlen - self.utils.__len__(feature)))
		for feature in features:
			temp = []
			for vector in feature:
				if not type(vector).__module__ == numpy.__name__:
					temp.append(numpy.zeros((self.config.hidden_state,), dtype = numpy.float32))
				else: temp.append(vector)
			padded_observations.append(temp)
		return padded_observations

	def matrix_transform(self, features, learning_apprach = None, divisor: int = 32):
		transformed = []
		if self.config.hidden_state % divisor == 0:
			cols = self.config.hidden_state // divisor
			shape = (divisor, cols)
			for feature in features:
				pass
			TODO
		else:
			raise ValueError

	def _pipeline(self):
		TODO
		pass