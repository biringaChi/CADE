import os
from src.utils import Utils
from setuptools import setup

setup(
	name = "CADE",
	description = "Context-Aware Detection of Embedded Credentials",
	license = "MIT License",
	author = "Chidera 'Chi' Biringa",
	author_email = "biringachidera@gmail.com",
	url = "https://github.com/biringaChi/CADE",
	install_requires = [req.rstrip() for req in Utils.reader(os.getcwd(), "requirements.txt")],
	python_requires = ">=3.9.0"
)