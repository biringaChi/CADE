import logging

class Logger:
	def __call__(self) -> None:
		pass

	@classmethod
	def _debug(self):
		pass

	@classmethod
	def _info(self, message):
		logging.basicConfig(level = logging.INFO)
		logging.info(message)

	@classmethod
	def _warning(self):
		pass

	@classmethod
	def _error(self):
		pass

	@classmethod
	def _critical(self):
		pass

	