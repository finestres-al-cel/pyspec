#!/usr/bin/env python

import glob
import git

from setuptools import find_namespace_packages, setup
from pathlib import Path

scripts = sorted(glob.glob('bin/*py'))

description = (f"pyspec\n"
               f"commit hash: {git.Repo('.').head.object.hexsha}")
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

exec(open('pyspec/_version.py').read())
version = __version__

setup(name="pyspec",
    version=version,
    description=description,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/finestres-al-cel/pyspec",
    author="Ignasi Pérez-Ràfols",
    author_email="iprafols@gmail.com",
    packages=find_namespace_packages(where='pyspec'),
    install_requires=['astropy', 'matplotlib', 'scipy', 'pyqt6'
                      'gitpython'],
    scripts = scripts
    )
