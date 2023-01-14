from __future__ import division

import os
import re
import torch
import numpy as np
from utils import Utils as ut
from typing import Tuple, Union
from sklearn.model_selection import train_test_split
from torch.utils.data import TensorDataset, DataLoader

class FeatureHandler:
	def __init__(self, feature_dir: str = os.getcwd() + "/features/") -> None:
		self.ut = ut.config()["metacols"]
		self.clf = ut.config()["clf_params"]
		self.feature_dir = feature_dir
	
	def contextual_features(self) -> np.ndarray[float]:
		secrets, benign = ut.unpickle(self.feature_dir + "secrets.pickle"), ut.unpickle(self.feature_dir + "benign.pickle")
		return np.concatenate((secrets, benign))
	
	def binary_class_encoder(self) -> np.ndarray[float]:
		secrets = [self.clf["pos_lab"] for _ in range(self.ut["obslen"])]
		benign = [self.clf["neg_lab"] for _ in range(self.ut["obslen"])]
		return np.array(secrets + benign)
	
	def multivariable_class_encoder(self): 
		pass

	def data_loader(self, X, y) -> torch.FloatTensor:
		return DataLoader(
				TensorDataset(
				torch.from_numpy(X), torch.from_numpy(y)
				), 
				shuffle = True, 
				batch_size = self.clf["batch_size"]
		)

	def retrieve_observations(self, algo: str = "mlalgo") -> Union[Tuple[np.ndarray[float]], Tuple[torch.FloatTensor]]:
		X_train, X_test, y_train, y_test = train_test_split(
			self.contextual_features(), 
			self.class_encoder(), 
			test_size = self.clf["test_size"], 
			random_state = self.clf["random_state"]
			)
		if re.match(algo, self.clf["mlalgo"], re.IGNORECASE):
			return X_train, X_test, y_train, y_test
		else: 
			sample = self.ut["obslen"] // self.clf["sample"]
			X_val, y_val, X_test, y_test = X_test[sample:], y_test[sample:], X_test[:sample], y_test[:sample]
			return (
				self.data_loader(X_train, y_train),
				self.data_loader(X_val, y_val),
				self.data_loader(X_test, y_test)
			)

class ClassEncoder:
	def __init__(self) -> None:
		pass
	