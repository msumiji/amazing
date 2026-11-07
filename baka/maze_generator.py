import sys
import random
from pathlib import Path
import configparser
from typing import List, Tuple, Set, Dict

# 壁のビットフラグ定義 (北:1, 東:2, 南:4, 西:8)
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
ALL_WALLS = NORTH | EAST | SOUTH | WEST  # 15 (16進数表記で 'f')

# 移動方向と対応する壁のビット、対向の壁のビット、方角文字
DIRECTIONS = [
    (0, -1, NORTH, SOUTH, 'N'),  # 上
    (1, 0, EAST, WEST, 'E'),     # 右
    (0, 1, SOUTH, NORTH, 'S'),  # 下
    (-1, 0, WEST, EAST, 'W')     # 左
]

# ANSIカラー定義
COLORS = {
    "green": "\033[32m",
    "cyan": "\033[36m",
    "yellow": "\033[33m",
    "magenta": "\033[35m",
    "reset": "\033[0m"
}
COLOR_LIST = list(COLORS.values())[:-1]


class MazeGenerator:
    def __init__(self, config_path: str = "config.txt"):
        self.config_path = config_path
        config = self._load_config()
        (
            self.width,
            self.height,
            self.perfect,
            self.entry,
            self.exit,
            self.output_file,
            self.seed
        ) = config
        self.rng = random.Random(self.seed)
        self.grid: List[List[int]] = []
        self.obstacle_cells: Set[Tuple[int, int]] = set()

        # 視覚表示・インタラクティブ用の状態管理
        self.show_path = False
        self.color_index = 0
        self.shortest_path_coords: List[Tuple[int, int]] = []
        self.shortest_path_str: str = ""

    def _load_config(
        self
    ) -> Tuple[int, int, bool, Tuple[int, int], Tuple[int, int], str, int | None]:
        """設定ファイルを読み込んで幅、高さ、PERFECTフラグ、ENTRY、EXIT、出力ファイル名を取得"""
        config = configparser.ConfigParser()
        if not Path(self.config_path).exists():
            return 9, 7, True, (0, 0), (8, 6), "output_maze.txt", None

        config.read(self.config_path)
        section = config.sections()[0] if config.sections() else 'DEFAULT'

        width = config.getint(section, 'WIDTH', fallback=15)
        height = config.getint(section, 'HEIGHT', fallback=10)
        perfect = config.getboolean(section, 'PERFECT', fallback=True)

        entry_str = config.get(section, 'ENTRY', fallback="0,0")
        exit_str = config.get(
            section,
            'EXIT',
            fallback=f"{width-1},{height-1}"
        )
        entry = tuple(map(int, entry_str.split(',')))
        exit_coord = tuple(map(int, exit_str.split(',')))
        seed = config.getint(section, 'SEED', fallback=None)

        output_file = config.get(
            section,
            "OUTPUT_FILE",
            fallback="output_maze.txt"
        ).strip()

        if not output_file:
            output_file = "output_maze.txt"

        return width, height, perfect, entry, exit_coord, output_file, seed

    def validate_and_place_42(self) -> bool:
        """42のパターンを配置する。ENTRYやEXITと重なる場合は位置を移動して配置する。"""
        pattern_width = 7
        pattern_height = 5

        # 迷路が小さすぎる場合
        if (self.width < pattern_width + 2 or
                self.height < pattern_height + 2):
            print(
                "Warning: '42' pattern has been omitted "
                "due to insufficient maze size.",
                file=sys.stderr
            )
            return False

        # 42の配置パターン
        four_coords = [
            (0, 0), (0, 1), (0, 2),
            (1, 2), (2, 2), (2, 3), (2, 4)
        ]

        two_coords = [
            (4, 0), (5, 0), (6, 0),
            (6, 1),
            (4, 2), (5, 2), (6, 2),
            (4, 3),
            (4, 4), (5, 4), (6, 4)
        ]

        pattern_coords = four_coords + two_coords
        entry_exit_cells = {self.entry, self.exit}

        # 標準の中央配置位置を基準にする
        center_x = (self.width - pattern_width) // 2
        center_y = (self.height - pattern_height) // 2

        # 中央を最優先とし、重なる場合に備えて周囲の候補位置（オフセット）を生成する
        candidates = [(center_x, center_y)]
        for dx in range(-4, 5):
            for dy in range(-4, 5):
                nx, ny = center_x + dx, center_y + dy
                # 迷路の枠内（外周を避ける範囲）に収まるかをチェック
                if 1 <= nx <= self.width - pattern_width - 1 and 1 <= ny <= self.height - pattern_height - 1:
                    if (nx, ny) not in candidates:
                        candidates.append((nx, ny))

        # 中央以外の候補をランダムにシャッフルして探索
        other_candidates = candidates[1:]
        self.rng.shuffle(other_candidates)
        candidates = [candidates[0]] + other_candidates

        placed = False
        cells = set()
        for start_x, start_y in candidates:
            current_cells = {
                (start_x + dx, start_y + dy)
                for dx, dy in pattern_coords
            }
            # ENTRY または EXIT と重ならない場所を探す
            if not (current_cells & entry_exit_cells):
                cells = current_cells
                placed = True
                break

        # どうしても置ける場所がない場合のみ省略
        if not placed:
            print(
                "Warning: '42' pattern has been omitted "
                "because no valid position was found without overlapping ENTRY or EXIT.",
                file=sys.stderr
            )
            return False

        # 42を配置
        for x, y in cells:
            self.grid[y][x] = ALL_WALLS
            self.obstacle_cells.add((x, y))

        return True

    def generate_maze(self) -> None:
        """非再帰の深さ優先探索（DFS）を用いて迷路の通路を確実に掘り進める"""
        self.grid = [[ALL_WALLS for _ in range(self.width)] for _ in range(self.height)]
        self.obstacle_cells.clear()
        self.validate_entry_exit()
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
                        nx, ny, wall_bit, opp_bit = self.rng.choice(neighbors)
                        self.grid[cy][cx] &= ~wall_bit
                        self.grid[ny][nx] &= ~opp_bit
                        visited[ny][nx] = True
                        stack.append((nx, ny))
                    else:
                        stack.pop()

        if not self.perfect:
            self.remove_dead_ends()

        # 迷路生成後に最短経路を探索して計算する
        self.solve_shortest_path()

    def solve_shortest_path(self) -> None:
        """幅優先探索 (BFS) を用いてENTRYからEXITまでの最短経路と方角文字列を算出する"""
        from collections import deque

        queue = deque([self.entry])
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
                # 壁が空いている（ビットが立っていない）場合のみ移動可能
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

        # 経路の復元
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

    def render(self) -> None:
        """迷路をアスキーアート形式でコンソールに描画する"""
        current_color = COLOR_LIST[self.color_index % len(COLOR_LIST)]
        reset = COLORS["reset"]

        print("\n" + "=" * 40)
        print(f" A-Maze-ing | Path: {'ON' if self.show_path else 'OFF'} | Size: {self.width}x{self.height}")
        print("=" * 40)

        print(current_color + "+" + "---+" * self.width + reset)

        for y in range(self.height):
            row_str = current_color + "|" + reset
            for x in range(self.width):
                cell_val = self.grid[y][x]

                content = "   "
                if (x, y) == self.entry:
                    content = " S "
                elif (x, y) == self.exit:
                    content = " E "
                elif (x, y) in self.obstacle_cells:
                    content = " 42"
                elif self.show_path and (x, y) in self.shortest_path_coords:
                    content = " . "

                east_wall = current_color + "|" + reset if (cell_val & EAST) else " "
                row_str += content + east_wall

            print(row_str)

            bottom_str = current_color + "+"
            for x in range(self.width):
                cell_val = self.grid[y][x]
                south_wall = "---" if (cell_val & SOUTH) else "   "
                bottom_str += south_wall + "+"
            print(bottom_str + reset)

    def export(self) -> None:
        """16進数フォーマットおよび最短経路情報を含めて迷路を出力"""
        lines = []
        for row in self.grid:
            hex_row = " ".join(format(cell, 'x') for cell in row)
            lines.append(hex_row)

        lines.append("")
        lines.append(f"{self.entry[0]},{self.entry[1]}")
        lines.append(f"{self.exit[0]},{self.exit[1]}")
        lines.append(self.shortest_path_str)

        Path(self.output_file).write_text("\n".join(lines) + "\n")

    def run_interactive(self) -> None:
        """インタラクティブメニューの実行ループ"""
        while True:
            self.render()
            print("\n=== A-Maze-ing Menu ===")
            print("1. Re-generate a new maze")
            print("2. Show/Hide the shortest path")
            print("3. Rotate the wall colours")
            print("4. Quit")

            choice = input("Choice? (1-4): ").strip()

            if choice == "1":
                self.generate_maze()
                self.export()
                print("\n> New maze generated and saved to output_maze.txt!")
            elif choice == "2":
                self.show_path = not self.show_path
                print(f"\n> Path visibility toggled to {self.show_path}")
            elif choice == "3":
                self.color_index += 1
                print("\n> Wall colors changed!")
            elif choice == "4":
                print("\nExiting A-Maze-ing. Goodbye!")
                break
            else:
                print("\n[Error] Invalid choice. Please enter a number between 1 and 4.")

    def remove_dead_ends(self) -> None:

        for y in range(self.height):
            for x in range(self.width):

            # 42の障害物は対象外
                if (x, y) in self.obstacle_cells:
                    continue

            # 現在のセルの通路数を数える
                cell = self.grid[y][x]

                passage_count = sum(
                    1 for _, _, wall_bit, _, _ in DIRECTIONS
                    if not (cell & wall_bit)
                )

            # 通路が1つでなければdead-endではない
                if passage_count != 1:
                    continue

            # 壁を取り除ける隣接セルを探す
                candidates = []

                for dx, dy, wall_bit, opp_bit, _ in DIRECTIONS:
                    nx = x + dx
                    ny = y + dy

                # 迷路の範囲内か確認
                    if not (0 <= nx < self.width and
                            0 <= ny < self.height):
                        continue

                # 42の障害物には接続しない
                    if (nx, ny) in self.obstacle_cells:
                        continue

                # まだ壁がある方向だけ候補にする
                    if self.grid[y][x] & wall_bit:
                        candidates.append(
                            (nx, ny, wall_bit, opp_bit)
                        )
            # 候補からランダムに1つ選んで壁を取り除く
                if candidates:
                    nx, ny, wall_bit, opp_bit = self.rng.choice(candidates)
                    self.grid[y][x] &= ~wall_bit
                    self.grid[ny][nx] &= ~opp_bit

    def validate_entry_exit(self) -> None:

        for name, (x, y) in [
            ("ENTRY", self.entry),
            ("EXIT", self.exit)
        ]:
            # 迷路の範囲内か確認
            if not (0 <= x < self.width and 0 <= y < self.height):
                raise ValueError(
                    f"{name} coordinate ({x},{y}) is outside "
                    f"the maze boundaries ({self.width}x{self.height})."
                )

        # 42の障害物と重なっていないか確認
            if (x, y) in self.obstacle_cells:
                raise ValueError(
                    f"{name} coordinate ({x},{y}) overlaps "
                    "with the '42' pattern."
                )
