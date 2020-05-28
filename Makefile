clean:
	find . -name '*.pyc' -exec rm -f {} +

init:
	pip install -r requirements.txt

test:
	python -m unittest -v