
################## INSTALLING ##################
PACKAGE_NAME = pymddoc

reinstall: uninstall install
	@echo "reinstalled"

uninstall:
	pip uninstall -y $(PACKAGE_NAME)

install:
	pip install .


################## DOCS ##################
REQUIREMENTS_FOLDER = ./requirements/
EXAMPLE_NOTEBOOK_FOLDER = ./examples/# this is where example notebooks are stored
EXAMPLE_NOTEBOOK_MARKDOWN_FOLDER = ./docs/documentation/# this is where example notebooks are stored

docs: readme requirements compile_examples mkdocs
	@echo "docs built"

serve_mkdocs: build_mkdocs
	mkdocs serve -a localhost:8882

mkdocs: build_mkdocs deploy_mkdocs
	# mkdocs build
	# mkdocs gh-deploy

deploy_mkdocs:
	mkdocs gh-deploy

build_mkdocs:
	mkdocs build

readme:
	python README.py

requirements:
	-mkdir $(REQUIREMENTS_FOLDER)
	pip freeze > $(REQUIREMENTS_FOLDER)/requirements.txt	
	pip list > $(REQUIREMENTS_FOLDER)/packages.txt

compile_examples:
	-mkdir $(EXAMPLE_NOTEBOOK_MARKDOWN_FOLDER)
	-jupyter nbconvert --to markdown $(EXAMPLE_NOTEBOOK_FOLDER)/*.ipynb
	-mv $(EXAMPLE_NOTEBOOK_FOLDER)/*.md $(EXAMPLE_NOTEBOOK_MARKDOWN_FOLDER)

	cd $(EXAMPLE_NOTEBOOK_FOLDER); \
		for FILE in *.py; do \
			echo "testing $$FILE"; \
			python $$FILE; \
		done


################## building ##################

build:
	# install latest version of compiler software
	pip install --user --upgrade setuptools wheel
	
	# actually set up package
	python setup.py sdist bdist_wheel
	
	git add setup.cfg setup.py LICENSE

clean_build:
	-rm -r $(PACKAGE_NAME).egg-info
	-rm -r dist
	-rm -r build

################## testing / linting ##################
test:
	cd tests; pytest *.py

mypy:
	python -m mypy pymddoc --python-version=3.11


