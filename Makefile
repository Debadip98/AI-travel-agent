.PHONY: help install test lint check run clean

help:
	@echo "AI Travel Agent - Makefile Commands"
	@echo "===================================="
	@echo "make install    - Install all dependencies"
	@echo "make test       - Run unit tests"
	@echo "make lint       - Run code linting"
	@echo "make check      - Run all pre-deployment checks"
	@echo "make run        - Start Streamlit app locally"
	@echo "make clean      - Clean cache and temporary files"

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

test:
	@echo "🧪 Running unit tests..."
	pytest tests/ -v

lint:
	@echo "🔍 Running linter..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	@echo "✅ No critical linting errors found"

check:
	@echo "🚀 Running pre-deployment checks..."
	@echo ""
	python test_agent.py
	@echo ""
	@echo "Running unit tests..."
	pytest tests/ -v
	@echo ""
	@echo "✅ All checks passed! Ready to deploy."

run:
	@echo "🚀 Starting Streamlit app..."
	streamlit run app.py

clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cleanup complete"
