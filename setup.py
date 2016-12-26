#!/usr/bin/python
from setuptools import setup

from hsluv import __version__

setup(
    name='hsluv',
    version=__version__,
    description='Human-friendly HSL',
    license="MIT",
    author_email="alexei@boronine.com",
    url="http://www.hsluv.org",
    keywords="color hsl cie cieluv colorwheel hsluv hpluv",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3"
    ],
    py_modules=["hsluv"],
    test_suite="tests.hsluv_test"
)
