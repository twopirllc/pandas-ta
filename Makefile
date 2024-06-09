.PHONY: tests
tests:
	pytest -vvv -s -l tests

caches:
	find pandas_ta -type d -name "__pycache__"
	find tests -type d -name "__pycache__"
	find __pycache__ -type d -name "__pycache__"

clean:
	find pandas_ta -type d -name "__pycache__" -exec rm -r {} +
	find tests -type d -name "__pycache__" -exec rm -r {} +
	find __pycache__ -type d -name "__pycache__" -exec rm -r {} +

init:
	pip install -r requirements.txt

test_metrics:
	pytest -vv -s -l -W ignore::DeprecationWarning --cache-clear tests/test_metrics.py

test_numba:
	pytest -vv -s -l -W ignore::DeprecationWarning --cache-clear tests/test_numba.py

test_studies:
	pytest -vv -s -l -W ignore::DeprecationWarning --cache-clear tests/test_studies.py

test_ta:
	pytest -vv -s -l -W ignore::DeprecationWarning --cache-clear tests/test_indicator_*.py

test_utils:
	pytest -vv -s -l -W ignore::DeprecationWarning --cache-clear tests/test_utils.py
