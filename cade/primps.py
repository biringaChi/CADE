import typing
import importlib as im
from pathlib import Path

def import_helper_modules() -> typing.Tuple[callable]:
	file_pth: str = Path.cwd().parents[0] / "helper"
	utils = im.util.spec_from_file_location("utils", file_pth / "utils.py")
	config = im.util.spec_from_file_location("config", file_pth / "config.py")
	return utils.loader.load_module().Utils,  config.loader.load_module().Config()