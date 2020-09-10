.PHONY: all
all:
	make test_ta
	make test_ext
	make test_strats

caches:
	find ./pandas_ta | grep -E "(__pycache__|\.pyc|\.pyo$\)"

clean:
	find . -name '*.pyc' -exec rm -f {} +

init:
	pip install -r requirements.txt

test_ta:
	python -m unittest -v tests/test_indicator_*.py

test_ext:
	python -m unittest -v tests/test_ext_indicator_*.py

test_strats:
	python -m unittest -v tests/test_strategy.py