#!/usr/bin/env python
import sys
import re

from setuptools import setup
from pypi2spec import __version__

description = "Automate the pypi to fedora package transition process"

long_description = """
Automate the rather annoying process of migrating a pypi package into
the fedora repos. This script uses pypingou's pypi2spec to generate
the original bare bones spec, and then takes care of everything from there
"""


requirements = [
    'pbs',
    'pypi2spec',
]


setup(
    name='pypi2fedora',
    version=__version__,
    description=description,
    author="Ross Delinger",
    author_email="rossdylan@csh.rit.edu",
    maintainer="Ross Delinger",
    maintainer_email="",
    url="http://github.com/rossdylan/pypi2fedora",
    license="GPLv3+",
    long_description=long_description,
    packages=['pypi2spec'],
    include_package_data=True,
    install_requires=requirements,
    entry_points="""
    [console_scripts]
    pypi2fedora = pypi2fedora:main
    """
)
