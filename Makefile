PYTHON ?= python3

.PHONY: test analyze

test:
	PYTHONPATH=src $(PYTHON) -m unittest discover -s tests -v

analyze:
	PYTHONPATH=src $(PYTHON) -m program_risk_board.cli analyze --data-file data/risks.json --export-dir reports
