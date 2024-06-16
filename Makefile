install:
	pip install --upgrade pip &&\
		pip install -r requirements.txt

test:
	python -m pytest -vv 

format:	
	black app/*.py 

lint:
	pylint --disable=R,C app/*.py
		
all: install lint format test

activate:
	source /home/vscode/venv/bin/activate