#### build

#### deploy

####  start at local for debug

start-spring-webmvc-local:
	@:

### setup environment for local

init-python:
	python -m pip install pipenv
	@if [ -z "$(python -m pip list --disable-pip-version-check | grep pyenv)" ]; then \
		curl https://pyenv.run | bash \
	fi

test:
	python -m pytest

doc:
	python -m pydoc -b

style: flake8 black

flake8:
	python -m flake8

black:
	python -m black --target-version=py37 --check ./	

install:
	pipenv install --dev
	pipenv run flake8 --version
	pipenv run pytest --version

shell:
	pipenv shell

clean:
	pipenv clean
	pipenv --rm

uninstall:
	rm -rf ~/.pyenv
	pip3 uninstall pipenv
