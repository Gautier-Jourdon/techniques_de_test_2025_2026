.PHONY: install test run-manager run-triangulator clean

install:
	pip install -r requirements.txt
	pip install -r dev_requirements.txt

test:
	python -m unittest discover tests

run-manager:
	python server/start_servers.py manager

run-triangulator:
	python server/start_servers.py triangulator

clean:
	rm -rf __pycache__
	rm -rf TP/modules/__pycache__
	rm -rf tests/__pycache__
	rm -rf tests/unit/__pycache__
	rm -rf tests/integration/__pycache__
