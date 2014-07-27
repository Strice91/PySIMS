import sys
from cx_Freeze import setup, Executable

setup(
	name = "PySIMS",
	version = "0.1",
	description = "PySIMS",
	targetName = "PySIMS.exe",
	executables = [Executable("PySIMS.py")]
)
