# 変数定義
PYTHON = python3
PIP = pip
LINT = flake8
MYPY = mypy
TARGET = a_maze_ing.py
CONFIG = config.txt

.PHONY: all install run debug lint clean

all: run

install:
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) $(TARGET) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(TARGET) $(CONFIG)

lint:
	$(LINT) *.py
	$(MYPY) *.py

clean:
	rm -rf __pycache__ .mypy_cache .pytest_cache
	find . -type f -name "*.pyc" -delete
	rm -f output_maze.txt