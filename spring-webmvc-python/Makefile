#### build

#### deploy

####  start at local for debug

start-spring-webmvc-local:
	@:

### setup environment for local

init-python:
	python3 -m pip install pipenv
	curl https://pyenv.run | bash
        
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
