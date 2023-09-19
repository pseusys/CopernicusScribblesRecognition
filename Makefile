.ONESHELL:
.DEFAULT_GOAL := help

SHELL = /bin/bash
PATH := venv/bin:$(PATH)


help:
	@ # Display help information
	echo "Copernicus scribbles recognition tool"
.PHONY: help

venv:
	@ # Create python virtual environment
	python3 -m venv venv
	pip3 install --upgrade pip jupyter~=1.0
	pip3 install -r requirements.txt
	jupyter nbextension enable --py widgetsnbextension

run-notebooks: venv
	@ # Run and save all the notebooks
	jupyter nbconvert --execute --to notebook --inplace sources/*.ipynb
.PHONY: run-notebooks

clean:
	@ # Clean all temporary files
	rm -rf venv
	rm -rf sources/cache
	rm -rf sources/datasets
	rm -rf **/__pycache__
.PHONY: clean
