.PHONY: help venv test clean
help:
	@echo "Available  commands:"
	@echo "  venv   - Create a virtual environment"
	@echo "  test   - Run tests"
	@echo "  clean  - Remove cache and temporary files"

venv:
	python3 -m venv .venv

test:
	pytest tests/ -v

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	rm -rf .pytest_cache
