clean:
	find . -name '*.pyc' -exec rm -f {} +

caches:
	find ./pandas_ta | grep -E "(__pycache__|\.pyc|\.pyo$\)"

init:
	pip install -r requirements.txt

ti:
	python -m unittest -v tests/test_indicator*.py

ts:
	python -m unittest -v tests/test_strategy.py