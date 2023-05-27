.PHONY: test
test:
	pytest -vv -s -l tests

caches:
	find ./pandas_ta | grep -E "(__pycache__|\.pyc|\.pyo$\)"

clean:
	find . -name '*.pyc' -exec rm -f {} +

init:
	pip install -r requirements.txt

test_metrics:
	pytest -vv -s -l --cache-clear tests/test_metrics.py

test_studies:
	pytest -vv -s -l --cache-clear tests/test_studies.py

test_ta:
	pytest -vv -s -l --cache-clear tests/test_indicator_*.py

test_utils:
	pytest -vv -s -l --cache-clear tests/test_utils.py