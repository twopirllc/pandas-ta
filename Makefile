clean:
	find . -name '*.pyc' -exec rm -f {} +

caches:
	find ./pandas_ta | grep -E "(__pycache__|\.pyc|\.pyo$\)"

init:
	pip install -r requirements.txt

test:
	python -m unittest -v