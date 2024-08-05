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

build:
	docker build -t mkeohane01/baseball-agent:latest .
run:
	docker run -p 3000:3000 mkeohane01/baseball-agent:latest

push:
	docker push mkeohane01/baseball-agent:latest

docker: build run

llamafile:
	bash run_llama_model.sh

