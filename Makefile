PYTHON ?= python3

.PHONY: test
test:
	$(PYTHON) -m unittest discover -s skills/job-search-discovery/scripts -p 'test_*.py'
	$(PYTHON) -m unittest discover -s skills/job-apply/scripts -p 'test_*.py'
	$(PYTHON) -m unittest discover -s skills/resume-update/scripts -p 'test_*.py'
	$(PYTHON) -m unittest discover -s tests -p 'test_*.py'
