""" Setup module """
from os.path import abspath, dirname, join
from setuptools import find_packages, setup

from argos import __version__

this_dir = abspath(dirname(__file__))

with open(join(this_dir, 'README.md'), encoding='utf-8') as f:
  long_desc = f.read()

with open(join(this_dir, 'requirements.txt'), encoding='utf-8') as f:
  reqs = f.read().splitlines()

setup(
    name='argos',
    version=__version__,
    description='Data gathering and analysis',
    long_description=long_desc,
    long_description_content_type="text/markdown",
    url='https://github.com/Melk0rr/Argos',
    author='Jaufré Lallement',
    author_email='lallement.j.pro@proton.me',
    classifiers=['Intended Audience :: Developers',
                 'Topic :: Utilities',
                 'License :: Public Domain',
                 'Operating System :: OS Independent',
                 'Programming Language :: Python :: 3.10', ],
    keywords='cli',
    packages=find_packages(exclude=['docs', 'tests*']), python_requires='>=3',
    install_requires=[reqs],
    entry_points={'console_scripts': ['argos=argos.cli:main', ], },
    py_modules=["argos.utils", "argos.scanners"],
)
