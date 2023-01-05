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

class BERTCLF(torch.nn.Module):
	def __init__(self) -> None:
		super(BERTCLF, self).__init__()
		self.bert_config = ut.config()
		self.activation_func = torch.nn.Sigmoid()
		self.dropout = torch.nn.Dropout(self.bert_config["bert-config"]["dropout"]) 
		self.BERT = transformers.BertModel.from_pretrained("bert-base-uncased")
		self.fully_connected = torch.nn.Linear(self.bert_config["bert-config"]["out_features"], self.bert_config["bert-config"]["label"]) 

	def forward(self, input_ids, attention_mask, token_type_ids = None):
		_, out = self.BERT(input_ids, attention_mask, output_all_encoded_layers = False)
		out = self.dropout(out)
		out = self.fully_connected(out)
		out = self.activation_func(out)
		return out

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