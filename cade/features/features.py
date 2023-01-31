import os
from utils import Utils as ut
from typing import List, Tuple
from simpletransformers.language_representation import RepresentationModel

class ContextualFeatures:
	def __init__(self) -> None:
		self.ut = ut.config()["metacols"]
		self.BERT = ut.config()["bert"]
		self.directory = os.getcwd() + "/benchmark/" 

	def raw_data(self) -> Tuple[List[str]]:
		return (
			ut.cleaner(ut.reader(self.directory, self.ut["sn"])[:self.ut["obslen"]]), 
			ut.cleaner(ut.reader(self.directory, self.ut["bn"])[:self.ut["obslen"]])
		)
	
	def BERT(self, data: List[str]) -> List[float]:
		model = RepresentationModel(
			model_type = self.BERT["model_type"], 
			model_name = self.BERT["model_name"], 
			use_cuda = False
		)
		return model.encode_sentences(
			data, 
			combine_strategy = self.BERT["combine_strategy"]
			)

if __name__ == "__main__":
	featuresdir = f"{os.getcwd()}/features/"
	cf = ContextualFeatures()
	secrets, benign = cf.raw_data()
	ut.pickle(cf.BERT(secrets), featuresdir + "secrets")
	ut.pickle(cf.BERT(benign), featuresdir + "benign")