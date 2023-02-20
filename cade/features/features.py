import typing
import pathlib
import argparse
import importlib
from simpletransformers.language_representation import RepresentationModel

parser = argparse.ArgumentParser(description = "Generates Contextual Embedding Features")
parser.add_argument(
	"-c", 
	"--cred", 
	type = str, 
	metavar = "", 
	required = True, 
	help = "Enter credential category"
	)
args = parser.parse_args()

class ContextualEmbeddings:
	"""
	Contextual Feature Embeddings Generator. 
	
	"""
	def __init__(self) -> None:
		self.im_mod = importlib.util.spec_from_file_location("primps", pathlib.Path.cwd().parents[0]/"primps.py")
		self.utils, self.config, self.logger = self.im_mod.loader.load_module().import_helper_modules()
		self.navigator, self.location = self.utils.navigator()["credentials"], self.utils.navigator()["dataobjects"]
	
	def __str__(self) -> str:
		return self.__class__.__name__
	
	def __repr__(self) -> str:
		return self.__str__()
	
	def password(self) -> typing.Text:
		return self.utils.reader(self.navigator, self.config.p_password)

	def generic_secret(self) -> typing.Text:
		return self.utils.reader(self.navigator, self.config.g_generic_secret)

	def private_key(self) -> typing.Text:
		return self.utils.reader(self.navigator, self.config.p_private_key)

	def predefined_pattern(self) -> typing.Text:
		return self.utils.reader(self.navigator, self.config.p_predefined_pattern)

	def seed_salt_nonce(self) -> typing.Text:
		return self.utils.reader(self.navigator, self.config.s_seed_salt_nonce)

	def generic_token(self) -> typing.Text:
		return self.utils.reader(self.navigator, self.config.g_generic_token)

	def auth_key_token(self) -> typing.Text:
		return self.utils.reader(self.navigator, self.config.a_auth_key_token)
	
	def other(self) -> typing.Text:
		return self.utils.reader(self.navigator, self.config.o_other)
	
	def credential(self) -> typing.Text:
		return self.utils.reader(self.navigator, self.config.credentials)
	
	def non_credentials(self) -> typing.Text: 
		return self.utils.reader(self.navigator, self.config.non_credentials)
	
	@property
	def get_credentials(self) -> typing.Dict:
		return {
			self.password.__name__ : self.password(), 
			self.generic_secret.__name__ : self.generic_secret(),
			self.private_key.__name__ : self.private_key(),
			self.predefined_pattern.__name__ : self.predefined_pattern(),
			self.seed_salt_nonce.__name__ : self.seed_salt_nonce(),
			self.generic_token.__name__ : self.generic_token(),
			self.auth_key_token.__name__ : self.auth_key_token(),
			self.other.__name__ : self.other()
		}
	
	def __getitem__(self, credential):
		return self.get_credentials[credential]

	def _fine_tune(self,
		data, 
		batch_size,
		model_type = None,
		model_name = None,
		combine_strategy = None
		) -> None:
		model = RepresentationModel(
			model_type = self.config.model_type,
			model_name = self.config.model_name, 
			use_cuda = False
		)
		return model.encode_sentences(data, batch_size)

if __name__ == "__main__":
	CE = ContextualEmbeddings()
	credential = CE[args.cred]
	CE.logger._info("Fine-tuning begins")
	CE.utils.pickle(CE._fine_tune(credential, CE.utils.__len__(credential)) , CE.location / args.cred.__repr__().strip("'"))
	CE.logger._info("Fine-tuning concludes")