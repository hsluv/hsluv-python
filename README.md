[![Build Status](https://github.com/hsluv/hsluv-python/actions/workflows/test.yml/badge.svg)](https://github.com/hsluv/hsluv-python/actions/workflows/test.yml)
[![Package Version](https://img.shields.io/pypi/v/hsluv.svg)](https://pypi.python.org/pypi/hsluv/)
[![PyPI Downloads](https://img.shields.io/pypi/dm/hsluv.svg)](https://pypistats.org/packages/hsluv)

A Python implementation of [HSLuv](https://www.hsluv.org) (revision 4).

## Installation

`pip install hsluv`

Python 2 users: `pip install hsluv==5.0.0`

## Usage

> This library does not hide (clamp) floating point error, e.g. you might receive a value outside
> of the expected range. If you wish to display the outputs of this library, consider rounding them 
> for your purpose. The floating point error has not been quantified, but at least 10 decimal digits 
> should be free of it.

### `hsluv_to_hex([hue, saturation, lightness])`

`hue` is a float between 0 and 360, `saturation` and `lightness` are floats between 0 and 100. This 
function returns the resulting color as a hex string.

### `hsluv_to_rgb([hue, saturation, lightness])`

Like above, but returns a list of 3 floats between 0 and 1, for each RGB channel.

### `hex_to_hsluv(hex)`

Takes a hex string and returns the HSLuv color as a list of floats as defined above.

### `rgb_to_hsluv([red, green, blue])`

Like above, but `red`, `green` and `blue` are passed as floats between 0 and 1.

For HPLuv (the pastel variant), use `hpluv_to_hex`, `hpluv_to_rgb`, `hex_to_hpluv` and `rgb_to_hpluv`.

## Testing

Run `python -m unittest discover -v`.

## Publishing to PyPI

Configure the GitHub environment and PyPI Trusted Publisher before publishing:

* In `hsluv/hsluv-python` on GitHub, open **Settings → Environments → New environment**.
* Name the environment **`pypi`** and click **Configure environment**. If it already exists, open it instead.
* Under **Deployment protection rules**, enable **Required reviewers**, select trusted release reviewers, and save the rules. Only one listed reviewer needs to approve a deployment.
* Enable **Prevent self-review** if a different person should approve the workflow initiator's deployment. Ensure another reviewer is available before enabling it.
* Under **Deployment branches and tags**, choose **Selected branches and tags** and add a branch rule for **`main`** to restrict publishing to that branch.
* If these protection options are unavailable, check GitHub's plan and repository-visibility requirements before relying on approval enforcement.
* As a PyPI project Owner, open the `hsluv` project's **Manage → Publishing** page and add a GitHub Trusted Publisher with owner **`hsluv`**, repository **`hsluv-python`**, workflow **`publish.yml`**, and environment **`pypi`**. No API token or GitHub secret is needed.

To publish a release:

* Update `__version__` in `hsluv.py` to an unused version, such as `5.0.5rc1` for a pre-release, and merge the change into `main` after tests pass.
* Open **Actions → Publish to PyPI → Run workflow**, select **`main`**, and click **Run workflow**. This uploads to production PyPI, including for pre-release versions; a tag or GitHub release is not required.
* If approval is required, have an eligible reviewer open the workflow run, click **Review deployments**, select **`pypi`**, and click **Approve and deploy**.
* Wait for the workflow to succeed, then verify the version on [PyPI](https://pypi.org/project/hsluv/) and install it with `python -m pip install 'hsluv==5.0.5rc1'` (substitute the version being released).
* Never reuse a published version: PyPI does not allow replacing uploaded distribution files, even after deletion.

## Authors

* Robert McGinley ([mcginleyr1](https://github.com/mcginleyr1))
* Alexei Boronine ([boronine](https://github.com/boronine))
* Sebastian Pipping ([hartwork](https://github.com/hartwork))
