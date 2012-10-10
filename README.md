[![Build Status](https://secure.travis-ci.org/boronine/pyhusl.png)](http://travis-ci.org/boronine/pyhusl)

Work in progress to port [HUSL](https://github.com/boronine/husl) to Python. Port started by Robert McGinley and released under the same license as HUSL.

## Usage

**husl_to_hex(hue, saturation, lightness)**

`hue` is a float between 0 and 360, `saturation` and `lightness` are floats between 0 and 100. This function returns the resulting color as a hex string.

**husl_to_rgb(hue, saturation, lightness)**

Like above, but returns a list of 3 numbers between 0 and 1, for each RGB channel.

**hex_to_husl(hex)**

Takes a hex string and returns the HUSL color as a list of floats as defined above.

**rgb_to_husl(red, green, blue)**

Like above, but `red`, `green` and `blue` are passed as floats between 0 and 1.

## Testing

Run `pip install -r requirements.txt` and `python setup.py test`.

## Authors

* Robert McGinley ([mcginleyr1](http://github.com/mcginleyr1))
* Alexei Boronine ([boronine](http://github.com/boronine))

***

Copyright (C) 2012 Alexei Boronine

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
