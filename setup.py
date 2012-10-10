#!/usr/bin/python

# Use setuptools if we can
try:
    from setuptools.core import setup
except ImportError:
    from distutils.core import setup
from husl import __version__

setup(
    name = 'husl',
    version = __version__,
    description = 'Human-friendly HSL',
    license = "MIT",
    author_email = "alexei.boronine@gmail.com",
    url = "http://github.com/boronine/pyhusl",
    keywords = "color hsl cie cieluv colorwheel",
    classifiers = [
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Software Development"
    ],
    py_modules = ["husl"],
    test_suite = "tests.husl_test"
)
