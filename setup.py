#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Setup Parallel WaveGAN libarary."""

import os
import pip
import sys

from distutils.version import LooseVersion
from setuptools import find_packages
from setuptools import setup

if LooseVersion(sys.version) < LooseVersion("3.6"):
    raise RuntimeError(
        "parallel-wavegan requires Python>=3.6, "
        "but your Python is {}".format(sys.version))

dirname = os.path.dirname(__file__)
setup(name="parallel_wavegan",
      version="0.2.8",
      url="http://github.com/erogol/ParallelWaveGAN",
      author="Eren Gölge",
      description="Parallel WaveGAN implementation",
      long_description=open(os.path.join(dirname, "README.md"),
                            encoding="utf-8").read(),
      long_description_content_type="text/markdown",
      license="MIT License",
      packages=find_packages(include=["parallel_wavegan*"]),
      install_requires=[
        "torch==1.4.0",
        "numpy==1.15.4",
        "scipy==1.4.1",
        "librosa==0.7.2",
      ],
      classifiers=[
          "Programming Language :: Python :: 3.6",
          "Programming Language :: Python :: 3.7",
          "Intended Audience :: Science/Research",
          "Operating System :: POSIX :: Linux",
          "License :: OSI Approved :: MIT License",
          "Topic :: Software Development :: Libraries :: Python Modules"],
      )
