# Catalogue Digital Editions

* static version of https://dig-ed-cat.acdh.oeaw.ac.at/
* see discussion https://github.com/acdh-oeaw/dig_ed_cat/issues/244

## install

* clone the repo
* change into the project's root directory e.g. `cd dig-ed-cat-static`
* create a virtual environment e.g. `python -m venv venv` and activate it `source venv/bin/activate`
* install required packages `pip install -r requirements.txt`
* run `python build_static.py` to build the website
* to test the result, change into `html` and start a python server `python -m http.server`


-----

This project was bootstraped by [python-static-cookiecutter](https://github.com/acdh-oeaw/python-static-cookiecutter)