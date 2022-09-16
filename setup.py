import sys
import os
from cx_Freeze import setup, Executable

# ADD FILES
files = ['icon.ico','themes/']

# TARGET
target = Executable(
    script="main.py",
    base="Win32GUI",
    icon="icon.ico"
)

# SETUP CX FREEZE
setup(
    name = "Self",
    version = "0.1",
    description = "Application for Productivity and Focus in Study",
    author = "Leonardo Ferreira N. da Silva",
    options = {'build_exe' : {'include_files' : files}},
    executables = [target]
)
