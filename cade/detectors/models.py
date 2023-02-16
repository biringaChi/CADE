import torch
from typing import Dict
import sklearn

from utils import Utils as ut
import transformers
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

class MLP:
	pass

class LSTM(torch.nn.Module):
	# TODO
	pass

class GRU(torch.nn.Module):
	pass

class DBN(torch.nn.Module):
	pass

class BERTCORE(torch.nn.Module):
	def __init__(self, task: str = None) -> None:
		super(BERTCORE, self).__init__()
		self.task = task
		_, self.ml = ut.config()
		self.bert_config, self.default_config = self.ml["dl"]["bert"], self.ml["dl"]["default"]
		self.sigmoid = torch.nn.Sigmoid()
		self.dropout = torch.nn.Dropout(self.default_config["dropout"]) 
		self.BERT = transformers.BertModel.from_pretrained(self.bert_config["model_name"])

		self.binary = self.default_config["target_binary"]
		self.multivariate = self.default_config["target_multivariate"]
		self.out_features = self.default_config["out"]
		
		self.fully_connected_binary = torch.nn.Linear(self.out_features, self.binary) 
		self.fully_connected_multivariate = torch.nn.Linear(self.out_features, self.multivariate) 

	def forward(self, input_ids, attention_mask, token_type_ids = None):
		_, out = self.BERT(input_ids, attention_mask, output_all_encoded_layers = False)
		out = self.dropout(out)


		out = self.fully_connected_binary(out)
		bout = self.sigmoid(out)
		mout = self.fully_connected_multivariate(self.out_features, self.multivariate) 
		return out
 
class CNN(torch.nn.Module):
	def __init__(self):
		super(CNN, self).__init__()
		_, self.ml = ut.config()
		self.cnn_params = self.ml["dl"]["cnn"]
		self.flatten = torch.nn.Flatten()
		self.clf_layer = torch.nn.Sigmoid()
		self.dropout = torch.nn.Dropout(self.cnn_params["dropout"])

		self.first_layer = torch.nn.Sequential(
			torch.nn.Conv2d(self.cnn_params["in_channels"], self.cnn_params["out_channels"], self.cnn_params["kernel"], self.cnn_params["stride"], 
			self.cnn_params["padding"]), torch.nn.LeakyReLU(), torch.nn.AdaptiveMaxPool2d(self.cnn_params["pool"]))
		self.second_layer = torch.nn.Sequential(
			torch.nn.Conv2d(self.cnn_params["in_channels"], self.cnn_params["out_channels"], self.cnn_params["kernel"], self.cnn_params["stride"], 
			self.cnn_params["padding"] + 1), torch.nn.LeakyReLU(), torch.nn.AdaptiveMaxPool2d(self.cnn_params["pool"]))

		self.fc = torch.nn.Linear(self.cnn_params["in_features"] * self.cnn_params["in_features"], self.cnn_params["out_features"])
		self.fcbinary = torch.nn.Linear(self.cnn_params["out_features"], self.cnn_params["label"]) # sigmoid

		# self.multivariate

		self.model = torch.nn.Sequential(
			self.first_layer,
			self.second_layer,
			self.flatten,
			self.dropout,
			self.fc,
			self.dropout,
			# self.fc2,
		)

def forward(self, features):
	return self.model(features)

class MlClfs:
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