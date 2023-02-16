import importlib
import pathlib
from setuptools import setup

setup(
	name = "CADE",
	description = "Context-Aware Detection of Embedded Credentials",
	license = "MIT License",
	author = "Chidera 'Chi' Biringa",
	author_email = "biringachidera@gmail.com",
	url = "https://github.com/biringaChi/CADE",
	python_requires = ">=3.9.0",
	install_requires = [req.rstrip() for req in importlib.util.spec_from_file_location("utils", pathlib.Path.cwd() / "cade" / "helper" / "utils.py").loader.load_module().Utils.reader(pathlib.Path.cwd(), "requirements.txt")]
)