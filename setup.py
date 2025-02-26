#!/usr/bin/env python

# ----------------------------------------------------------------------------
# Copyright (c) 2016--, BacDivePy development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file COPYING.txt, distributed with this software.
# ----------------------------------------------------------------------------

import re
import ast
import os
import pip
from setuptools import find_packages, setup
from setuptools.command.build_ext import build_ext as _build_ext


class build_ext(_build_ext):
    def finalize_options(self):
        _build_ext.finalize_options(self)
        # Prevent numpy from thinking it is still in its setup process:
        __builtins__.__NUMPY_SETUP__ = False
        import numpy
        self.include_dirs.append(numpy.get_include())


# Dealing with Cython
USE_CYTHON = os.environ.get('USE_CYTHON', False)
ext = '.pyx' if USE_CYTHON else '.c'

extensions = [
]

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions)

classes = """
    Development Status :: 3 - Alpha
    License :: OSI Approved :: BSD License
    Topic :: Software Development :: Libraries
    Topic :: Scientific/Engineering
    Topic :: Scientific/Engineering :: Bio-Informatics
    Programming Language :: Python :: 3
    Programming Language :: Python :: 3 :: Only
    Operating System :: Unix
    Operating System :: POSIX
    Operating System :: MacOS :: MacOS X
"""
classifiers = [s.strip() for s in classes.split('\n') if s]

description = ('Python API Interface for DSMZ BacDive')

with open('README.md') as f:
    long_description = f.read()


# version parsing from __init__ pulled from Flask's setup.py
# https://github.com/mitsuhiko/flask/blob/master/setup.py
_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('bacdive/__init__.py', 'rb') as f:
    hit = _version_re.search(f.read().decode('utf-8')).group(1)
    version = str(ast.literal_eval(hit))

setup(name='bacdive',
      version=version,
      license='BSD',
      description=description,
      long_description=long_description,
      author="BacDivePy development team",
      author_email="cameronmartino@gmail.com",
      maintainer="BacDivePy development team",
      maintainer_email="cameronmartino@gmail.com",
      packages=find_packages(),
      setup_requires=['numpy >= 1.9.2'],
      ext_modules=extensions,
      cmdclass={'build_ext': build_ext},
      install_requires=[
          'numpy',
          'IPython >= 3.2.0',
          'matplotlib >= 1.4.3',
          'numpy >= 1.12.1',
          'pandas >= 0.10.0',
          'scipy >= 0.19.1',
          'nose >= 1.3.7',
          'scikit-bio >= 0.5.1',
          'seaborn >= 0.9.0',
          'tqdm'],classifiers=classifiers,package_data={})
