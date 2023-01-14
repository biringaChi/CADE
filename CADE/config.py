from utils import Utils

class Config:
	def __init__(self) -> None:
		self.default, self.ml = Utils.config()

		self.metadata = self.default["metadata"]
		self.fp = self.metadata["fp"]
		self.lsle = self.metadata["lsle"]
		self.gt = self.metadata["gt"]
		self.cat = self.metadata["cat"]
		self.sn = self.metadata["sn"]
		self.cat = self.metadata["cat"]
		self.obslen = self.metadata["obslen"]

		self.negative = self.default["groundtruth"]
		self.positive = self.default["groundtruth"]
		self.partial_positive = self.default["partial_positive"]

		self.category = self.default["category"]
		self.password = self.default["password"]
		self.private_key = self.default["private_key"]
		self.generic_token = self.default["generic_token"]
		self.generic_secret = self.default["generic_secret"]
		self.predefined_pattern = self.default["predefined_pattern"]
		self.seed_salt_nonce = self.default["seed_salt_nonce"]
		self.other = self.other["other"]

		self.gen = self.ml["dl"]["default"]
		self.max_iter = self.gen["max_iter"]
		self.solver = self.gen["solver"]
		self.mlalgo = self.gen["mlalgo"]
		self.dlalgo = self.gen["dlalgo"]
		self.batch_size = self.gen["batch_size"]
		self.pos_lab = self.gen["pos_lab"]
		self.neg_lab = self.gen["neg_lab"]
		self.random_state = self.gen["random_state"]
		self.test_size = self.gen["test_size"]
		self.sample = self.gen["sample"]
		self.dropout = self.gen["dropout"]
		self.label_binary = self.gen["label_binary"]
		self.label_multivariable = self.gen["label_multivariable"]

		self.trainer = self.ml["dl"]["trainer"]
		self.epochs = self.trainer["epochs"]



