import torch
import typing
import sklearn
import transformers

class RF:
	def __call__(self):
		return sklearn.ensemble.RandomForestClassifier()

class SVM:
	def __call__(self, max_iter):
		return sklearn.svm.LinearSVC(max_iter = max_iter)

class NB:
	def __call__(self):
		return sklearn.naive_bayes.GaussianNB()

class KNN:
	def __call__(self):
		return sklearn.neighbors.KNeighborsClassifier()

class LR:
	def __call__(self, *lr):
		solver, max_iter = lr
		return sklearn.linear_model.LogisticRegression(solver = solver, max_iter = max_iter)

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
	def __init__(self, *cnn):
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