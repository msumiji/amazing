import random


def dig(
    x: int,
    y: int,
    width: int,
    height: int,
    maze: list[list[str]]
) -> None:
    maze[y][x] = " "

    directions = [
        (0, -2),
        (0, 2),
        (-2, 0),
        (2, 0)
    ]

    random.shuffle(directions)

    for dx, dy in directions:
        nx = x + dx
        ny = y + dy

        if (0 < nx < width - 1
                and 0 < ny < height - 1
                and maze[ny][nx] == "#"):

            maze[y + dy // 2][x + dx // 2] = " "

            dig(nx, ny, width, height, maze)


def main() -> None:
    w = 10
    h = 10
    width = 2 * w + 1
    height = 2 * h + 1

    maze = [["#" for _ in range(width)] for _ in range(height)]

    dig(1, 1, width, height, maze)

    maze[1][1] = "S"
    maze[height - 2][width - 2] = "G"

    for row in maze:
        print("".join(row))


if __name__ == "__main__":
    main()
