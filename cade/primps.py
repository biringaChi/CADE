import typing
import pathlib
import importlib

def import_helper_modules() -> typing.Tuple[callable]:
	file_pth: str = pathlib.Path.cwd().parents[0]/"helper"
	utils = importlib.util.spec_from_file_location("utils", file_pth/"utils.py")
	config = importlib.util.spec_from_file_location("config", file_pth/"config.py")
	return utils.loader.load_module().Utils, config.loader.load_module().Config()
	