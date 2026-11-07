import sys
import random
from maze_generator import MazeGenerator


def main() -> None:
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
