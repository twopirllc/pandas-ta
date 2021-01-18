.PHONY: all
all:
	make test_utils
	make test_metrics
	make test_ta
	make test_ext
	make test_strats

caches:
	find ./pandas_ta | grep -E "(__pycache__|\.pyc|\.pyo$\)"

clean:
	find . -name '*.pyc' -exec rm -f {} +

init:
	pip install -r requirements.txt

test_ext:
	python -m unittest -v -f tests/test_ext_indicator_*.py

test_metrics:
	python -m unittest -v -f tests/test_utils_metrics.py

test_strats:
	python -m unittest -v -f tests/test_strategy.py

test_ta:
	python -m unittest -v -f tests/test_indicator_*.py

test_utils:
	python -m unittest -v -f tests/test_utils.py
	python -m unittest -v -f tests/test_utils_metrics.py