[![Build Status](https://travis-ci.org/husl-colors/husl-python.svg?branch=master)](http://travis-ci.org/husl-colors/husl-python)
[![Package Version](https://img.shields.io/pypi/v/husl.svg)](https://pypi.python.org/pypi/husl/)

A Python implementation of [HUSL](http://www.husl-colors.org) (revision 3).

## Installation

`pip install husl`

## Usage

**husl_to_hex(hue, saturation, lightness)**

`hue` is a float between 0 and 360, `saturation` and `lightness` are floats between 0 and 100. This function returns the resulting color as a hex string.

**husl_to_rgb(hue, saturation, lightness)**

Like above, but returns a list of 3 floats between 0 and 1, for each RGB channel.

**hex_to_husl(hex)**

Takes a hex string and returns the HUSL color as a list of floats as defined above.

**rgb_to_husl(red, green, blue)**

Like above, but `red`, `green` and `blue` are passed as floats between 0 and 1.

For HUSLp (the pastel variant), use `huslp_to_hex`, `huslp_to_rgb`, `hex_to_huslp` and `rgb_to_huslp`.

## Testing

Run `python setup.py test`.

## Authors

* Robert McGinley ([mcginleyr1](http://github.com/mcginleyr1))
* Alexei Boronine ([boronine](http://github.com/boronine))

