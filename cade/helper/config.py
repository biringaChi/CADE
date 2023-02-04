import typing
import importlib as im
from pathlib import Path as pth

class Config:
	"""
	Configurations
	"""
	def __init__(self) -> None:
		self.configs_pth: str = pth.cwd().parents[1] / "configs"
		self.utils_module = im.import_module("utils")
		self.utils = self.utils_module.Utils
		self.default, self.ml = self.utils.config([self.configs_pth / "default.json", self.configs_pth / "ml.json"])

		self.metadata: typing.Dict = self.default["metadata"]
		self.fp: str = self.metadata["fp"]
		self.lsle: str = self.metadata["lsle"]
		self.gt: str = self.metadata["gt"]
		self.credentials: str = self.metadata["credentials"]
		self.non_credentials: str = self.metadata["non_credentials"]

		self.groundtruth: typing.Dict = self.default["groundtruth"]
		self.positive: typing.List[str] = self.groundtruth["positive"]
		self.negative: typing.List[str] = self.groundtruth["negative"]
		self.partial: str = self.groundtruth["partial"]

		self.category: typing.Dict = self.default["category"]
		self.password: typing.List[str] = self.category["password"]
		self.private_key: typing.List[str] = self.category["private_key"]
		self.generic_token: typing.List[str] = self.category["generic_token"]
		self.generic_secret: typing.List[str] = self.category["generic_secret"]
		self.predefined_pattern: typing.List[str] = self.category["predefined_pattern"]
		self.seed_salt_nonce: typing.List[str] = self.category["seed_salt_nonce"]
		self.other: typing.List[str] = self.category["other"]

		self.mlml: typing.Dict = self.ml["ml"]
		self.beta: float = self.mlml["beta"]
		self.f1: str = self.mlml["f1_score"]
		self.precision: str = self.mlml["prec"]

		self.gen: typing.Dict = self.ml["dl"]["default"]
		self.max_iter: int = self.gen["max_iter"]
		self.solver: str = self.gen["solver"]
		self.mlalgo: str = self.gen["mlalgo"]
		self.dlalgo: str = self.gen["dlalgo"]
		self.batch_size: int = self.gen["batch_size"]
		self.positive_lab: int = self.gen["pos_lab"]
		self.negative_lab: int = self.gen["neg_lab"]
		self.password_lab: int = self.gen["pwd_lab"]
		self.generic_secret_lab: int = self.gen["gensec_lab"]
		self.private_key_lab: int = self.gen["privkey_lab"]
		self.generic_token: int = self.gen["gentok_lab"]
		self.predefined_pattern_lab: int = self.gen["predpath_lab"]
		self.auth_key_token_lab: int = self.gen["authkeytok_lab"]
		self.seed_salt_nonce_lab: int = self.gen["sesano_lab"]
		self.other_lab: int = self.gen["other"]
		self.random_state: int = self.gen["random_state"]
		self.test_size: float = self.gen["test_size"]
		self.sample: int = self.gen["sample"]
		self.dropout: float = self.gen["dropout"]
		self.binary_task_lab: int = self.gen["label_binary"]
		self.multiclass_task_lab: int = self.gen["label_multivariate"]

		self.trainer: typing.Dict = self.ml["dl"]["trainer"]
		self.epochs: int = self.trainer["epochs"]
		self.learning_rate: float = self.trainer["learning_rate"]
		self.betas: typing.List[float] = self.trainer["betas"]

		self.cnn_params: typing.Dict = self.ml["dl"]["cnn"]
		self.in_channels: int = self.cnn_params["in_channels"]
		self.out_channels: int = self.cnn_params["out_channels"]
		self.in_features: int = self.cnn_params["in_features"]
		self.out_features: int = self.cnn_params["out_features"]
		self.kernel: int = self.cnn_params["kernel"]
		self.stride: int = self.cnn_params["stride"]
		self.padding: int = self.cnn_params["padding"]
		self.pooling: int = self.cnn_params["pooling"]

		self.bert_params: typing.Dict = self.ml["dl"]["bert"]
		self.model_type: str = self.bert_params["model_type"]
		self.model_name: str = self.bert_params["model_name"]
		self.combine_strategy: typing.List[str] = self.bert_params["combine_strategy"]