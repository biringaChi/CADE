import torch
import typing
import sklearn
import transformers

class RF:
	# TODO
	def __call__(self):
		pass

class SVM:
	# TODO
	def __call__(self):
		pass

class NB:
	# TODO
	def __call__(self):
		pass

class KNN:
	# TODO
	def __call__(self):
		pass

class LR:
	# TODO
	def __call__(self):
		pass

class MLP:
	# TODO
	def __call__(self):
		pass

class LSTM(torch.nn.Module):
	# TODO
	def __call__(self):
		pass

class GRU(torch.nn.Module):
	# TODO
	def __call__(self):
		pass

class DBN(torch.nn.Module):
	# TODO
	def __call__(self):
		pass
 
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

		# TODO --> multivariate

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


class Core(torch.nn.Module):
	def __init__(self, task: str = None) -> None:
		super(Core, self).__init__()
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