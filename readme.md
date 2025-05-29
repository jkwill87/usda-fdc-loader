# usda-fdc-loader

A utility which can be used to download, extract, parse, and transform [USDA Food Data Central](https://fdc.nal.usda.gov) datasets into a consistent format suitable for importing and integration.

## Setup

* Clone repo, e.g. `git clone https://github.com/jkwill87/usda-fdc-loader.git`
* Configure [config.yml](config.yml)

## Running

### Using uv

* `uv run -m foodprep`

### Using venv

* Set up a virtualenv: `python3 -m venv .venv`
* Activate the virtualenv: `source .venv/bin/activate` (shell dependant)
* Install runtime requirements: `pip3 install -r requirements.txt`
* Run the python module within the working directory: `python3 -m foodprep`

## License

MIT. See [license.txt](license.txt) for details.
