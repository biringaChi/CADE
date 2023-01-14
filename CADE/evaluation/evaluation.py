from utils import Utils as ut
from detectors import Detectors
from featurehandler import FeatureHandler as fh
from imblearn.metrics import geometric_mean_score 
from sklearn.model_selection import cross_validate
from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score, fbeta_score

class Evaluation(Detectors):
	def __init__(self) -> None:
		super().__init__()
		self.fh = fh()
		self.params = ut.config()["meval"]
	
	def metrics(self):
		return {
			"f1_score" : self.params["f1_score"],
			"fbeta" : make_scorer(fbeta_score, beta = self.params["beta"]), 
			"precision" : self.params["precision"], 
			"recall" : "recall",
			"specificity" : make_scorer(recall_score, pos_label = 0), 
			"gmean" :  make_scorer(geometric_mean_score, greater_is_better = True, average = "binary")
		}


class Analysis:
	pass