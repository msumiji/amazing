import os
from pathlib import Path

# プロジェクトに必要な全ファイルの内容を定義
files = {
    "LICENSE.md": """MIT License

Copyright (c) 2026 42 Student

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""",

    "README.md": """*This project has been created as part of the 42 curriculum by student.*

# A-Maze-ing (迷路生成 & 可視化パッケージ)

## 概要 (Description)

A-Maze-ing は、Python で実装された迷路生成および可視化ツールです。単一パスの完全迷路 (Perfect Maze) と、ループ経路を含み Pac-Man などのゲームに適したプレイ可能ボード (Pac-Man Mode) の双方の生成に対応しています。生成結果は 16 進数の壁フラグ形式で出力されるほか、再利用可能な Python ライブラリ (`mazegen`) としてパッケージ化されています。

## 使い方 (Instructions)

### 1. 仮想環境の構築と依存関係のインストール

```bash
make install
```

### 2. プログラムの実行

```bash
make run
# または直接実行:
python3 a_maze_ing.py config.txt
```

### 3. パッケージのビルド

```bash
make pkg-build
```

### 4. リンター・静的解析の実行

```bash
make lint
```

## 設定ファイルのフォーマット (Configuration File Format)

設定ファイルは `KEY=VALUE` 形式で記述します。`#` で始まる行はコメントとして無視されます。

```ini
[DEFAULT]
WIDTH = 20
HEIGHT = 20
PERFECT = True
ENTRY = 0,0
EXIT = 19,19
OUTPUT_FILE = output_maze.txt
SEED = 42
```

- **WIDTH / HEIGHT**: 迷路の幅と高さ (セル数)。
- **PERFECT**: `True` で完全迷路 (1つのパスのみ)、`False` でループありのプレイ可能ボード。
- **ENTRY / EXIT**: スタート位置およびゴール位置の座標 `x,y`。
- **OUTPUT_FILE**: 迷路データを出力するファイル名。
- **SEED**: (任意) 迷路生成を再現するための乱数シード。

## アルゴリズム (Generation Algorithm)

迷路の生成には **深さ優先探索 (DFS / Recursive Backtracking)** の非再帰実装を使用しています。

### 選定理由

- **高効率**: 計算量 $O(V + E)$ で動作し、スタック構造によりメモリ効率に優れます。
- **完全な連結性**: 独立したセルを発生させず、すべての通路が連結していることを保証します。
- **Pac-Man モードとの相性**: DFS で生成した基本構造から特定の壁を除去することで、簡単かつ確実に健全なループ構造へ拡張できます。

## 再利用可能パッケージ (`mazegen`)

迷路生成ロジックは `src/mazegen` 配下に隔離され、独立したモジュールとして利用可能です。

### インストール方法

```bash
pip install mazegen-1.0.0-py3-none-any.whl
```

### 使用例

```python
from mazegen import MazeGenerator

# パラメータを指定してインスタンス化
generator = MazeGenerator(width=15, height=15, perfect=True, seed=42)
generator.generate_maze()

# 生成データの取得
grid = generator.grid
shortest_path = generator.shortest_path_str
print("最短経路:", shortest_path)
```

## チームと役割 (Team & Management)

- **役割**: 個人開発 (設計、実装、テスト、パッケージ化)
- **開発経過**: DFS による完全迷路生成からスタートし、壁除去アルゴリズムによる Pac-Man モードの追加、MyPy/Flake8 適合、ならびに Python パッケージング (`setuptools`) の整備を行いました。
""",

    "pyproject.toml": """[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[project]
name = "mazegen"
version = "1.0.0"
description = "42 A-Maze-ing プロジェクト用 迷路生成ライブラリ"
readme = "README.md"
requires-python = ">=3.10"
license = {file = "LICENSE.md"}
authors = [
    {name = "42 Student", email = "student@42.fr"}
]
classifiers = [
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]

[project.optional-dependencies]
dev = ["flake8", "mypy"]
""",

    "config.txt": """[DEFAULT]
WIDTH = 20
HEIGHT = 20
PERFECT = True
ENTRY = 0,0
EXIT = 19,19
OUTPUT_FILE = output_maze.txt
SEED = 42
""",

    "Makefile": """VENV = .venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
LINT = $(VENV)/bin/flake8
MYPY = $(VENV)/bin/mypy
TARGET = a_maze_ing.py
CONFIG = config.txt
BUILD_DIR = dist

.PHONY: all install run debug lint clean pkg-build pkg-clean

all: run

install:
	python3 -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install build flake8 mypy

run:
	$(PYTHON) $(TARGET) $(CONFIG)

debug:
	$(PYTHON) -m pdb $(TARGET) $(CONFIG)

lint:
	$(LINT) src/ *.py
	$(MYPY) --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs src/ *.py

pkg-build:
	$(PYTHON) -m build
	cp $(BUILD_DIR)/mazegen-1.0.0-py3-none-any.whl ./

clean: pkg-clean
	rm -rf $(VENV)
	rm -rf __pycache__ .mypy_cache .pytest_cache
	find . -type f -name "*.pyc" -delete
	rm -f output_maze.txt

pkg-clean:
	rm -rf build/ $(BUILD_DIR)/ *.egg-info mazegen-*.whl mazegen-*.tar.gz
""",

    "src/mazegen/__init__.py": '"""迷路生成パッケージ."""\n\nfrom .generator import MazeGenerator\n\n__all__ = ["MazeGenerator"]\n',

    "src/mazegen/generator.py": '''"""迷路生成コアモジュール."""

from collections import deque
import configparser
from pathlib import Path
import random
import sys
from typing import Dict, List, Optional, Set, Tuple

# 壁のビットフラグ定義 (北:1, 東:2, 南:4, 西:8)
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
ALL_WALLS = NORTH | EAST | SOUTH | WEST

# 移動方向の定義 (dx, dy, 自セルの壁, 隣接セルの壁, 方角文字)
DIRECTIONS = [
    (0, -1, NORTH, SOUTH, 'N'),
    (1, 0, EAST, WEST, 'E'),
    (0, 1, SOUTH, NORTH, 'S'),
    (-1, 0, WEST, EAST, 'W')
]


class MazeGenerator:
    """迷路生成および解析を担当するコアクラス."""

    def __init__(
        self,
        width: int = 15,
        height: int = 10,
        perfect: bool = True,
        entry: Tuple[int, int] = (0, 0),
        exit_coord: Tuple[int, int] = (14, 9),
        output_file: str = "output_maze.txt",
        seed: Optional[int] = None
    ) -> None:
        """迷路パラメータの初期化."""
        self.width = width
        self.height = height
        self.perfect = perfect
        self.entry = entry
        self.exit = exit_coord
        self.output_file = output_file
        self.seed = seed

        if self.seed is not None:
            random.seed(self.seed)

        self.grid: List[List[int]] = []
        self.obstacle_cells: Set[Tuple[int, int]] = set()

        self.show_path = False
        self.color_index = 0
        self.shortest_path_coords: List[Tuple[int, int]] = []
        self.shortest_path_str: str = ""

    @classmethod
    def from_config(cls, config_path: str) -> "MazeGenerator":
        """設定ファイルから MazeGenerator インスタンスを生成する."""
        config = configparser.ConfigParser()
        path = Path(config_path)

        if not path.exists():
            print(f"警告: 設定ファイル {config_path} が見つかりません。デフォルト値を使用します。", file=sys.stderr)
            return cls()

        try:
            config.read(config_path, encoding="utf-8")
            section = config.sections()[0] if config.sections() else 'DEFAULT'

            width = config.getint(section, 'WIDTH', fallback=15)
            height = config.getint(section, 'HEIGHT', fallback=10)
            perfect = config.getboolean(section, 'PERFECT', fallback=True)

            entry_str = config.get(section, 'ENTRY', fallback="0,0")
            exit_str = config.get(section, 'EXIT', fallback=f"{width-1},{height-1}")

            entry = tuple(map(int, entry_str.split(',')))
            exit_coord = tuple(map(int, exit_str.split(',')))

            output_file = config.get(section, "OUTPUT_FILE", fallback="output_maze.txt").strip()
            if not output_file:
                output_file = "output_maze.txt"

            seed_val = config.get(section, 'SEED', fallback=None)
            seed = int(seed_val) if seed_val is not None else None

            if not (0 <= entry[0] < width and 0 <= entry[1] < height):
                entry = (0, 0)
            if not (0 <= exit_coord[0] < width and 0 <= exit_coord[1] < height):
                exit_coord = (width - 1, height - 1)

            return cls(
                width=width,
                height=height,
                perfect=perfect,
                entry=(entry[0], entry[1]),
                exit_coord=(exit_coord[0], exit_coord[1]),
                output_file=output_file,
                seed=seed
            )
        except Exception as err:
            print(f"エラー: 設定ファイルの読み込みに失敗しました ({err})。デフォルト値を使用します。", file=sys.stderr)
            return cls()

    def validate_and_place_42(self) -> bool:
        """'42' パターンを迷路の中央に配置する."""
        pattern_width = 7
        pattern_height = 5

        if self.width < pattern_width + 2 or self.height < pattern_height + 2:
            print(
                f"エラー: 迷路のサイズ ({self.width}x{self.height}) が小さすぎるため '42' パターンを配置できません。",
                file=sys.stderr
            )
            print("警告: サイズ不足のため '42' パターンは省略されます。", file=sys.stderr)
            return False

        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2

        four_coords = [(0, 0), (0, 1), (0, 2), (1, 2), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4)]
        two_coords = [(4, 0), (5, 0), (6, 0), (6, 1), (4, 2), (5, 2), (6, 2), (4, 3), (4, 4), (5, 4), (6, 4)]

        for dx, dy in four_coords + two_coords:
            px, py = start_x + dx, start_y + dy
            if py < self.height and px < self.width:
                self.grid[py][px] = ALL_WALLS
                self.obstacle_cells.add((px, py))

        return True

    def generate_maze(self) -> None:
        """非再帰 DFS を用いて迷路を生成する."""
        self.grid = [[ALL_WALLS for _ in range(self.width)] for _ in range(self.height)]
        self.obstacle_cells.clear()

        self.validate_and_place_42()

        visited = [[False for _ in range(self.width)] for _ in range(self.height)]

        for (ox, oy) in self.obstacle_cells:
            visited[oy][ox] = True

        for start_y in range(self.height):
            for start_x in range(self.width):
                if visited[start_y][start_x]:
                    continue

                stack = [(start_x, start_y)]
                visited[start_y][start_x] = True

                while stack:
                    cx, cy = stack[-1]

                    neighbors = []
                    for dx, dy, wall_bit, opp_bit, _ in DIRECTIONS:
                        nx, ny = cx + dx, cy + dy
                        if 0 <= nx < self.width and 0 <= ny < self.height:
                            if not visited[ny][nx]:
                                neighbors.append((nx, ny, wall_bit, opp_bit))

                    if neighbors:
                        nx, ny, wall_bit, opp_bit = random.choice(neighbors)
                        self.grid[cy][cx] &= ~wall_bit
                        self.grid[ny][nx] &= ~opp_bit
                        visited[ny][nx] = True
                        stack.append((nx, ny))
                    else:
                        stack.pop()

        if not self.perfect:
            self.add_loops()

        self.solve_shortest_path()

    def add_loops(self) -> None:
        """Pac-Man モード (PERFECT=False) 用に壁を取り除いてループを作成する."""
        candidates = []

        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.obstacle_cells:
                    continue

                if x + 1 < self.width and (x + 1, y) not in self.obstacle_cells:
                    if self.grid[y][x] & EAST:
                        candidates.append((x, y, EAST, WEST, x + 1, y))

                if y + 1 < self.height and (x, y + 1) not in self.obstacle_cells:
                    if self.grid[y][x] & SOUTH:
                        candidates.append((x, y, SOUTH, NORTH, x, y + 1))

        random.shuffle(candidates)
        loop_count = max(2, (self.width * self.height) // 25)

        for x, y, wall, opp_wall, nx, ny in candidates[:loop_count]:
            self.grid[y][x] &= ~wall
            self.grid[ny][nx] &= ~opp_wall

    def solve_shortest_path(self) -> None:
        """幅優先探索 (BFS) により ENTRY から EXIT までの最短経路を求める."""
        queue: deque[Tuple[int, int]] = deque([self.entry])
        parent: Dict[Tuple[int, int], Tuple[Tuple[int, int], str]] = {self.entry: ((-1, -1), "")}
        visited = {self.entry}

        found = False
        while queue:
            cx, cy = queue.popleft()

            if (cx, cy) == self.exit:
                found = True
                break

            cell_val = self.grid[cy][cx]
            for dx, dy, wall_bit, _, char in DIRECTIONS:
                if not (cell_val & wall_bit):
                    nx, ny = cx + dx, cy + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        if (nx, ny) not in visited:
                            visited.add((nx, ny))
                            parent[(nx, ny)] = ((cx, cy), char)
                            queue.append((nx, ny))

        if not found:
            self.shortest_path_coords = []
            self.shortest_path_str = ""
            return

        path_coords = []
        path_chars = []
        curr = self.exit
        while curr != self.entry:
            path_coords.append(curr)
            prev, char = parent[curr]
            path_chars.append(char)
            curr = prev
        path_coords.append(self.entry)
        path_coords.reverse()
        path_chars.reverse()

        self.shortest_path_coords = path_coords
        self.shortest_path_str = "".join(path_chars)

    def export(self) -> None:
        """16進数表記および解経路の情報をファイルへ出力する."""
        lines = []
        for row in self.grid:
            hex_row = " ".join(format(cell, 'x') for cell in row)
            lines.append(hex_row)

        lines.append("")
        lines.append(f"{self.entry[0]},{self.entry[1]}")
        lines.append(f"{self.exit[0]},{self.exit[1]}")
        lines.append(self.shortest_path_str)

        Path(self.output_file).write_text("\n".join(lines) + "\n", encoding="utf-8")
''',

    "a_maze_ing.py": '''"""A-Maze-ing メイン実行スクリプト."""

import sys
from typing import List
from mazegen import MazeGenerator

# ANSIカラー定義
COLORS = {
    "green": "\033[32m",
    "cyan": "\033[36m",
    "yellow": "\033[33m",
    "magenta": "\033[35m",
    "reset": "\033[0m"
}
COLOR_LIST: List[str] = list(COLORS.values())[:-1]


class MazeVisualizer:
    """MazeGenerator の端末描画およびメニュー操作を担当するクラス."""

    def __init__(self, generator: MazeGenerator) -> None:
        """初期化."""
        self.gen = generator

    def render(self) -> None:
        """迷路を ASCII アート形式で画面出力する."""
        current_color = COLOR_LIST[self.gen.color_index % len(COLOR_LIST)]
        reset = COLORS["reset"]

        mode_str = "PERFECT" if self.gen.perfect else "PAC-MAN"
        print("\n" + "=" * 45)
        print(f" A-Maze-ing [{mode_str}] | Path: {'ON' if self.gen.show_path else 'OFF'} | Size: {self.gen.width}x{self.gen.height}")
        print("=" * 45)

        print(current_color + "+" + "---+" * self.gen.width + reset)

        for y in range(self.gen.height):
            row_str = current_color + "|" + reset
            for x in range(self.gen.width):
                cell_val = self.gen.grid[y][x]

                content = "   "
                if (x, y) == self.gen.entry:
                    content = " S "
                elif (x, y) == self.gen.exit:
                    content = " E "
                elif (x, y) in self.gen.obstacle_cells:
                    content = " 42"
                elif self.gen.show_path and (x, y) in self.gen.shortest_path_coords:
                    content = " . "

                east_wall = current_color + "|" + reset if (cell_val & 2) else " "
                row_str += content + east_wall

            print(row_str)

            bottom_str = current_color + "+"
            for x in range(self.gen.width):
                cell_val = self.gen.grid[y][x]
                south_wall = "---" if (cell_val & 4) else "   "
                bottom_str += south_wall + "+"
            print(bottom_str + reset)

    def run_interactive(self) -> None:
        """インタラクティブ操作ループ."""
        while True:
            self.render()
            print("\n=== A-Maze-ing メニュー ===")
            print("1. 新しい迷路を再生成")
            print("2. 最短経路の表示 / 非表示 切り替え")
            print("3. 壁のカラーを変更")
            print("4. 終了")

            try:
                choice = input("選択してください (1-4): ").strip()
            except (KeyboardInterrupt, EOFError):
                print("\nプログラムを終了します。Goodbye!")
                break

            if choice == "1":
                self.gen.generate_maze()
                self.gen.export()
                print(f"\n> 新しい迷路を生成し、{self.gen.output_file} に保存しました！")
            elif choice == "2":
                self.gen.show_path = not self.gen.show_path
                print(f"\n> 経路表示を {'ON' if self.gen.show_path else 'OFF'} に変更しました。")
            elif choice == "3":
                self.gen.color_index += 1
                print("\n> 壁の色を変更しました！")
            elif choice == "4":
                print("\nプログラムを終了します。Goodbye!")
                break
            else:
                print("\n[エラー] 1〜4 の数字を入力してください。")


def main() -> None:
    """メイン処理関数."""
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config.txt"
    try:
        generator = MazeGenerator.from_config(config_file)
        generator.generate_maze()
        generator.export()

        visualizer = MazeVisualizer(generator)
        visualizer.run_interactive()
    except Exception as e:
        print(f"エラーが発生しました: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
'''
}


def setup_project() -> None:
    """定義した全ファイルを配置・更新する."""
    print("プロジェクト構築用のファイル一式を作成中...")
    for filepath, content in files.items():
        p = Path(filepath)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content, encoding="utf-8")
        print(f"  作成完了: {filepath}")
    print("\nファイル構成のセットアップが完了しました！")


if __name__ == "__main__":
    setup_project()