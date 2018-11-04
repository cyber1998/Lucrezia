import os
from setuptools import setup, find_packages

directory = os.path.dirname(os.curdir)
requirements_path = directory + "requirements.txt"
with open(requirements_path) as f:
    requirements = list(f.read().splitlines())
setup(
    name='lucrezia',
    version='1.0',
    py_modules=['main.py'],
    install_requires=requirements,
    entry_points='''
        [console_scripts]
        lucrezia=main:cli
    ''',
)