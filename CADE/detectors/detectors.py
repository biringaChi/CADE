import torch
from typing import Dict
import sklearn

from utils import Utils as ut
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

class Detectors:
	def __init__(self) -> None:
		self.params = ut.config()["clf_params"]

	def ml_clfs(self) -> Dict:
		return {
			GaussianNB().__class__.__name__ : GaussianNB(),
			KNeighborsClassifier().__class__.__name__ : KNeighborsClassifier(),
			RandomForestClassifier().__class__.__name__ : RandomForestClassifier(),
			LinearSVC().__class__.__name__ : LinearSVC(max_iter = self.params["max_iter"]),
			LogisticRegression().__class__.__name__  : LogisticRegression(solver = self.params["solver"], max_iter =  self.params["max_iter"])
		}

	def dl_clfs(self) -> Dict:
		return {
			CNN().__class__.__name__ : CNN(),
			MLPClassifier().__class__.__name__ : MLPClassifier(max_iter =  self.params["max_iter"]),
			# TODO: LSTM
			# TODO: GRU
			# TODO: DBN
		}

class LSTM(torch.nn.Module):
	# TODO
	pass

class GRU(torch.nn.Module):
	pass

class DBN(torch.nn.Module):
	pass


class CNN(torch.nn.Module):
	def __init__(self):
		super(CNN, self).__init__()
		self.params = ut.config()["cnn_params"]

		self.first_layer = torch.nn.Sequential(
			torch.nn.Conv1d(self.params["in_channels"], self.params["out_channels"], self.params["kernel"], self.params["stride"], 
			self.params["padding"]), torch.nn.LeakyReLU(), torch.nn.AdaptiveMaxPool1d(self.params["pool"]) 
		)
		self.second_layer = torch.nn.Sequential(
			torch.nn.Conv1d(self.params["in_channels"], self.params["out_channels"], self.params["kernel"], self.params["stride"], 
			self.params["padding"] + 1), torch.nn.LeakyReLU(), torch.nn.AdaptiveMaxPool1d(self.params["pool"]) 
		)
		self.third_layer = torch.nn.Sequential(
			torch.nn.Conv1d(self.params["in_channels"], self.params["out_channels"], self.params["kernel"], self.params["stride"], 
			self.params["padding"] + 2), torch.nn.LeakyReLU(), torch.nn.AdaptiveMaxPool1d(self.params["pool"]) 
		)
		
		self.fc1 = torch.nn.Linear(self.params["in_features"] * self.params["in_features"], self.params["out_features"])
		self.fc2 = torch.nn.Linear(self.params["out_features"], self.params["label"])

		self.dropout = torch.nn.Dropout(self.params["dropout"])
		self.flatten = torch.nn.Flatten()

		self.model = torch.nn.Sequential(
			self.first_layer,
			self.second_layer,
			self.third_layer,
			self.flatten,
			self.dropout,
			self.fc1,
			self.dropout,
			self.fc2,
			torch.nn.Sigmoid()
		)

def forward(self, features):
	return self.model(features)
