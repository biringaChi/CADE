import os
from src.utils import Utils
from setuptools import setup

setup(
	name = "BEWARE",
	description = "BERT-Assisted Detection of Secrets in GitHub Repositories",
	license = "GNU GENERAL PUBLIC LICENSE Version 3",
	author = "Chidera 'Chi' Biringa",
	author_email = "biringachidera@gmail.com",
	url = "https://github.com/biringaChi/BEWARE",
	install_requires = [req.rstrip() for req in Utils.reader(os.getcwd(), "requirements.txt")],
	python_requires = ">=3.9.0"
)