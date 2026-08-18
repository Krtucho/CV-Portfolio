.PHONY: install lint test scan secret-scan monitor

install:
	pip install -r requirements.txt

lint:
	ruff check scanners/ monitors/ crypto/ scripts/

test:
	pytest tests/ -v --cov=scanners --cov=monitors --cov=crypto

scan:
	python scanners/sast_scanner.py . --severity medium

secret-scan:
	python scanners/secret_scanner.py . --exclude-dir .git node_modules venv __pycache__

monitor:
	python monitors/threat_detector.py --input /var/log --rules rules/sigma --watch

dependency-scan:
	python scanners/dependency_scanner.py requirements.txt

report:
	python scripts/compliance_checker.py check --standard soc2 --target .

clean:
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
