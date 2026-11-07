# 変数定義
VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
LINT = $(VENV)/bin/flake8
MYPY = $(VENV)/bin/mypy
TARGET = main.py
CONFIG = config.txt

.PHONY: all install run debug lint clean

all: run

# 1. 仮想環境の作成と依存関係のインストール
install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	if [ -f requirements.txt ]; then $(PIP) install -r requirements.txt; fi

# 2. メインプログラムの実行
run:
	$(PYTHON) $(TARGET) $(CONFIG)

# 3. デバッグ実行
debug:
	$(PYTHON) -m pdb $(TARGET) $(CONFIG)

# 4. リンターの実行 (flake8 & mypy)
lint:
	$(LINT) *.py
	$(MYPY) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs *.py

lint-strict:
	$(LINT) *.py
	$(MYPY) --strict .

# 5. キャッシュや仮想環境、生成物の掃除
clean:
	rm -rf $(VENV)
	rm -rf __pycache__ .mypy_cache .pytest_cache
	find . -type f -name "*.pyc" -delete
	rm -f output_maze.txt
