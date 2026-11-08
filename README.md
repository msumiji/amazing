*This project has been created as part of the 42 curriculum by msumiji and ssagano*

# Description
In this project, we will do the following:
・Generate a random maze based on the information specified in config.txt.
・Place the number “42” in the center of the maze. The maze should be generated so that it avoids this number.
・Display the start and goal positions, and show the shortest path from the start to the goal.
You can freely configure the maze size, as well as the start and goal positions, by changing the values in config.txt. Furthermore, by changing the value of “PERFECT” in config.txt, you can toggle between a perfect maze (where there is only one path between any two points) and an imperfect maze (where there are multiple paths between any two points). In this project, dead ends (locations surrounded by walls on three sides) are also eliminated in imperfect mazes (excluding the location of the “42” character).

　Maze generation uses an algorithm called depth-first search (DFS). In this method, the program moves from the starting point to an adjacent unvisited cell and removes the wall in the direction of movement to create a path. This algorithm is explained below in accordance with the code for this project.
1. Initialize all cells as walls (line 175-178).
2. Place the character “42” (lines 179, 181).
3. Manage visited cells (line 183-186).
4. Start DFS from the starting point (lines 196, 197).
5. Search for adjacent unvisited cells (lines 202–209).
6. Randomly select one and remove the wall (lines 212–214).
7. Mark the destination as visited and add it to the stack (lines 215, 216).
8. If a dead end is reached, return (lines 217, 218).

　Another well-known algorithm for generating mazes is the “digging method.” In this method, a hole is dug from the starting point, and the program advances two squares at a time through unvisited areas. Consequently, the maze must have an odd number of rows and columns. Since this method cannot handle cases where the number of rows or columns is even as specified in config.txt, we determined it would be difficult to apply to this project; therefore, we adopted the DFS algorithm described above.

## Roles
  msumiji: Creating README.md, reviewing and revising the code.
  ssagano: Writing the main body of the code, creating LICENSE.md.

## Reflections on the Project
　This team was formed in August. However, since this project involved using a virtual environment, we decided to wait until one of the members had finished “python08,” so we didn’t actually get started until late October. Initially, since msumiji had finished Python08 first, the plan was for msumiji to take the lead on coding. However, since ssagano had a better understanding of the virtual environment, ssagano ended up taking the lead on coding.
　We struggled to balance eliminating dead ends with avoiding the creation of 3×3 open spaces. For a dead end blocked on three sides, we devised an algorithm that randomly selects and removes one of the three walls, but we also considered whether this might create a 3×3 open space. After drawing diagrams, I found it difficult to conceive of an example where removing a single wall from an overlapping dead-end would create an open space. Furthermore, after actually constructing an incomplete maze, I confirmed that no open spaces were created. Therefore, even without a rigorous proof, I concluded that open spaces cannot be formed.
Additionally, while the use of a virtual environment was strongly recommended for this project, I believe there was no point in using one since I relied solely on Python’s standard library.

# Instruction
make install: Installs the virtual environment. Run this command first before executing any other commands.

make run: Runs the program. When executed, a maze is displayed. Four options are also displayed simultaneously. Entering each number will execute the corresponding option. Selecting 1 generates a different maze. If the SEED value is fixed, the system is designed so that different mazes are always displayed in the same order. For example, if SEED is set to 42, selecting “Re-generate a new maze” will generate mazes in the order Maze A → Maze B → Maze C. However, if SEED is set to 41, the mazes will be generated in the order Maze D → Maze E → Maze F.

make debug: Uses pdb, the standard Python debugger. This allows you to execute the program one line at a time.

make clean: Deletes temporary files such as those created for the virtual environment and mypy_cache.

make lint: Runs checks using flake8 and mypy.  If you run `make lint-strict`, it will execute `mypy --strict .` simultaneously with flake8.

# Code Reusability
The maze program in this project is implemented as an independent, reusable module (`mazegen`) that can be imported and used in future projects. For example, consider using this project’s maze program in a Pac-Man game. In this case, all parts except those related to drawing the maze and displaying the interactive menu can be reused (via `.venv`). Specifically, these are the `render`, `export`, and `run_interactive` methods of the `MazeGenerator` class. The following explains how to import this program

## 1. How to Build the Package
When you run the `install` rule in the Makefile, the `build` and `wheel` packages are automatically installed within the virtual environment. You can use this to build the package and generate a `.whl` file using the following command:

### Install dependencies (includes build and wheel)
make install

### Activate the virtual environment and build the package
source .venv/bin/activate
python -m build

If the build is successful, a `dist/` directory will be created in the root directory, and a Wheel file will be generated.
Example: `dist/mazegen-1.0.0-py3-none-any.whl`

## 2. Installing and Using the Package
You can install the generated .whl file into any virtual environment or project using pip.
pip install dist/mazegen-1.0.0-py3-none-any.whl

# Resources
In creating this project, we drew on advice from students who entered the program at the same time as us. We happened to have many opportunities to review a_maze_ing, and during those sessions, they explained the project overview to us. We also utilized AI to write code and design algorithms.

# Description
　このプロジェクトでは以下のことを行います。
・config.txtに記載された情報に基づいてランダムに迷路を作る。
・迷路の中央に"42"の文字を入れる。迷路はこの文字を避けて作るようにする。
・スタートとゴールの位置を表示し、スタートからゴールまでの最短経路を表示する。
迷路の大きさ、スタート、ゴールの位置はconfig.txt内の値を書き換えることで自由に設定することができます。さらに、config.txt内の"PERFECT"の値を変えることで、迷路を完全迷路（2点間の経路が1つのみ）と不完全迷路（2点間の経路が複数ある）で切り替えることができます。本プロジェクトでは、さらに不完全迷路で袋小路（三方が壁で囲まれた場所）をなくしています（42の文字の場所は除く）。

　迷路生成は深さ優先探索（DFS）というアルゴリズムを使いました。この手法では、スタート地点から隣接する未訪問のマスへ移動し、移動した方向の壁を取り除いて通路を作ります。このアルゴリズムを本プロジェクトのコードに沿って以下説明します。
１．全てのマスを壁で初期化する(line 175-178)。
２．４２の文字を配置する(line 179,181)。
３．訪問済みマスを管理する(line 183-186)。
４．スタート地点からDFSを開始する(line 196,197)。
５．隣接する未訪問マスを探す(line 202-209)。
６．ランダムに1つ選んで壁を取り除く(line 212-214)。
７．移動先を訪問済みにしてスタックに追加する(line 215,216)。
８．行き止まりになったら戻る(line 217,218)。

　迷路生成の他のアルゴリズムとして有名なものに穴掘り法というのがあります。この手法では、スタート地点から穴を掘って未訪問の箇所を2マスずつ進みます。そのため、迷路の大きさは縦、横ともに奇数でなければならず、config.txtで縦あるいは横の大きさが偶数になった場合に対応できないため、本プロジェクトに適用するのに困難であると考えたため、上記のDFSを採用しました。

役割分担
msumiji：README.mdの作成、コードの確認、修正
ssagano：全体的なコードの作成、LICENSE.mdの作成

プロジェクトを通しての感想
　チーム結成は8月に行いました。しかし、本プロジェクトは仮想環境を使うということでしたので、メンバーのうちどちらかがpython08を終わってから行うという方針にし、実際の着手は10月後半になってからです。当初はmsumijiの方が先にpython08を終わらせたので、msumijiがコードの作成の主担当とする予定でしたが、ssaganoの方が仮想環境の理解ができていたので、コードの作成の主担当はssaganoの方が行git@github.com:msumiji/amazing.gitうことになりました。
　袋小路（dead-end）を消すことと、3×3のオープンスペースを作らないことを両立させるところは苦労しました。3方が塞がっている袋小路は3個の壁のどれかをランダムに選んで1つを消すというアルゴリズムにしたのですが、このときに3×3のオープンスペースができないかを検討しました。図面を書いて、袋小路が重なっている場所でどれか1つの壁を取り除いてもオープンスペースができる例が考えにくいことや、実際に不完全迷路を作ってみてオープンスペースができないことから、厳密な証明ができなくてもオープンスペースはできないものとしました。
　また、本プロジェクトでは、仮想環境を使うことが強く推奨されていましたが、本プロジェクトではpythonの標準ライブラリのみを使ったので仮想環境を使う意味はなかったと思います。

# Instruction
make install:仮想環境をインストールする。他のコマンドを実行する場合はまずこれを実行します。

make run:プログラムを実行する。実行すると迷路が表示される。同時に4つの選択肢も表示される。それぞれの数字を入力することで、選択肢の内容が実行される。1を選択すると、別の迷路が生成される。SEED値が固定されている場合は、必ず同じ順番で別の迷路が表示される仕組みになっている。例えば、SEED=42に設定している場合、Re-generate a new mazeを選択することで、迷路A→迷路B→迷路Cのように迷路が作られるが、SEED=41にすると、迷路D→迷路E→迷路Fの順番に作られます。

make debug:pythonに標準に備えられているデバッガーpdbを使う。これを使うとプログラムを1行だけ実行することができます。

make clean:仮想環境やmypy_cacheなどの一時的に作られたファイルを削除します。

make lint:flake8とmypyのチェックを行う。make lint-strictにすると、flake8と同時にmypy --strict .を実行します。

## Code Reusability
　本プロジェクトの迷路プログラムは、独立した再利用可能なモジュール（`mazegen`）として実装されており、将来のプロジェクトにインポートして使用することができます。例えば本プロジェクトの迷路プログラムをパックマンゲームに利用する場合を考えます。この場合、迷路の描画に関する箇所とインタラクティブメニューの表示以外の箇所は再利用.venv)することができます。具体的には、MazeGeneratorクラスのrender,export,run_interactiveメソッドの部分です。以下本プログラムをインポートする方法を解説します。

### 1. パッケージのビルド方法
Makefile の `install` 規則を実行すると、仮想環境内にwheel` パッケージが自動的にビルドされます。これを利用して、以下のコマンドでパッケージをビルドし、`.whl` ファイルを生成できます。

#### 依存関係のインストール（build と wheel が含まれます）
make install

#### 仮想環境を有効化してパッケージをビルド
source .venv/bin/activate
python -m build

ビルドが成功すると、ルート直下に dist/ ディレクトリが作成され、Wheel ファイルが生成されます。
生成例: dist/mazegen-1.0.0-py3-none-any.whl

### ２. パッケージのインストールと使用方法
生成された .whl ファイルは、pip を用いて任意の仮想環境やプロジェクトにインストールできます。
pip install dist/mazegen-1.0.0-py3-none-any.whl

## Resources
　このプロジェクトを作成するにあたって、同期入学の学生からの助言を利用しました。たまたまa_maze_ingのレビューをする機会がたくさんあり、その機会にa_maze_ingのプロジェクトの概要を教えてもらいました。また、コードの作成、アルゴリズムの構築にはAIを活用しました。
