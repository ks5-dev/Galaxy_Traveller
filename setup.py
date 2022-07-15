import sys
from cx_Freeze import setup, Executable

setup(
    name = "Galaxy Traveller",
    version = "1.1.0",
    description = "An arena shooter game made in pygame",
    executables = [Executable("menu.py")],
)