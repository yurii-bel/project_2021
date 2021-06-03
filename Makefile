install:
	python setup.py install

remove:
	pip uninstall timesoft -y

refactor:
	pip install black isort
	black timesoft/ examples/
	isort -rc timesoft/

upload:
	pip install twine
	python setup.py upload
