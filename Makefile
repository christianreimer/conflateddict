.PHONY: test flake clean install build

test: 
	pytest --cov-report term-missing --cov=conflateddict --verbose tests/*

flake:
	flake8 --max-complexity=10 --count

clean:
	@echo "Removing cache directories"
	@find . -name __pycache__ -type d -exec rm -rf {} +
	@find . -name .cache -type d -exec rm -rf {} +
	@find . -name .coverage -delete
	@find . -name build -type d -exec rm -rf {} +
	@find . -name dist -type d -exec rm -rf {} +
	@find . -name *egg-info -type d -exec rm -rf {} +

install:
	pip install -r requirements_test.txt

build:
	python setup.py sdist bdist_wheel
