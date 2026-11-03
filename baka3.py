import sys
import random
from pathlib import Path
import configparser
from typing import List, Tuple, Set

# 壁のビットフラグ定義 (北:1, 東:2, 南:4, 西:8)
NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8
ALL_WALLS = NORTH | EAST | SOUTH | WEST  # 15 (16進数表記で 'f')

# 移動方向と対応する壁のビット、対向の壁のビット
DIRECTIONS = [
    (0, -1, NORTH, SOUTH),  # 上
    (1, 0, EAST, WEST),     # 右
    (0, 1, SOUTH, NORTH),   # 下
    (-1, 0, WEST, EAST)     # 左
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
        self.width, self.height, self.perfect, self.entry, self.exit, self.output_file = self._load_config()
        self.grid: List[List[int]] = []
        self.obstacle_cells: Set[Tuple[int, int]] = set()

        # 視覚表示・インタラクティブ用の状態管理
        self.show_path = False
        self.color_index = 0
        self.dummy_path = []

    def _load_config(self) -> Tuple[int, int, bool, Tuple[int, int], Tuple[int, int]]:
        """設定ファイルを読み込んで幅、高さ、PERFECTフラグ、ENTRY、EXITを取得"""
        config = configparser.ConfigParser()
        if not Path(self.config_path).exists():
            return 9, 7, True, (0, 0), (8, 6), "maze.txt"

        config.read(self.config_path)
        section = config.sections()[0] if config.sections() else 'DEFAULT'

        width = config.getint(section, 'WIDTH', fallback=15)
        height = config.getint(section, 'HEIGHT', fallback=10)
        perfect = config.getboolean(section, 'PERFECT', fallback=True)

        entry_str = config.get(section, 'ENTRY', fallback="0,0")
        exit_str = config.get(section, 'EXIT', fallback=f"{width-1},{height-1}")

        entry = tuple(map(int, entry_str.split(',')))
        exit_coord = tuple(map(int, exit_str.split(',')))

        output_file = config.get(section, "OUTPUTFILE",
                         fallback="output_maze.txt").strip()

        if not output_file:
            output_file = "maze.txt"

        return width, height, perfect, entry, exit_coord, output_file

    def validate_and_place_42(self) -> bool:
        """
        '42' パターンを配置可能か検証し、迷路の中央に配置する。
        """
        pattern_width = 7
        pattern_height = 5

        if self.width < pattern_width + 2 or self.height < pattern_height + 2:
            print(
                f"Error: Maze size ({self.width}x{self.height}) is too small to fit the '42' pattern.",
                file=sys.stderr
            )
            print("Warning: '42' pattern has been omitted due to insufficient size.", file=sys.stderr)
            return False

        start_x = (self.width - pattern_width) // 2
        start_y = (self.height - pattern_height) // 2

        # 「4」の座標（右側の縦棒を下に1つ増やすため (2,4) を追加）
        four_coords = [(0,0), (0,1), (0,2), (1,2), (2,0), (2,1), (2,2), (2,3), (2,4)]

        # 「2」の座標（高さ6のバランスに合わせて調整、またはそのまま配置）
        two_coords = [(4,0), (5,0), (6,0), (6,1), (4,2), (5,2), (6,2), (4,3), (4,4), (5,4), (6,4)]

        for dx, dy in four_coords + two_coords:
            px, py = start_x + dx, start_y + dy
            if py < self.height and px < self.width:
                self.grid[py][px] = ALL_WALLS
                self.obstacle_cells.add((px, py))

        return True

    def generate_maze(self):
        """非再帰の深さ優先探索（DFS）を用いて迷路の通路を確実に掘り進める"""
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
                    for dx, dy, wall_bit, opp_bit in DIRECTIONS:
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
        self.dummy_path = [(x, x % self.height) for x in range(min(self.width, self.height))]

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
                elif self.show_path and (x, y) in self.dummy_path:
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

    def export(self):
        """16進数フォーマットで迷路を出力"""
        lines = []
        for row in self.grid:
            hex_row = " ".join(format(cell, 'x') for cell in row)
            lines.append(hex_row)

        lines.append("")
        lines.append(f"{self.entry[0]},{self.entry[1]}")
        lines.append(f"{self.exit[0]},{self.exit[1]}")
        lines.append("ESEENEEESSSEESESSESESSSSEEEEEESES")

        Path(self.output_file).write_text("\n".join(lines) + "\n")

    def run_interactive(self):
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

    def add_loops(self) -> None:
        candidates = []

        for y in range(self.height):
            for x in range(self.width):

            # 42のマスは対象外
                if (x, y) in self.obstacle_cells:
                    continue

            # 右隣との間の壁を調べる
                if x + 1 < self.width:
                    if (x + 1, y) not in self.obstacle_cells:
                        if self.grid[y][x] & EAST:
                            candidates.append((x, y, EAST, WEST))

            # 下隣との間の壁を調べる
                if y + 1 < self.height:
                    if (x, y + 1) not in self.obstacle_cells:
                        if self.grid[y][x] & SOUTH:
                            candidates.append((x, y, SOUTH, NORTH))

    # 壁を取り除く候補をランダムに並べる
        random.shuffle(candidates)

    # 取り除く壁の数
        loop_count = max(2, (self.width * self.height) // 50)

        for x, y, wall, opposite_wall in candidates[:loop_count]:

            if wall == EAST:
                nx, ny = x + 1, y
            else:
                nx, ny = x, y + 1

        # 隣接する2マスの間の壁を両方取り除く
            self.grid[y][x] &= ~wall
            self.grid[ny][nx] &= ~opposite_wall

def main():
    config_file = sys.argv[1] if len(sys.argv) > 1 else "config.txt"
    try:
        generator = MazeGenerator(config_file)
        generator.generate_maze()
        generator.export()
        generator.run_interactive()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
